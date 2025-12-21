#include <nanobind/nanobind.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/shared_ptr.h>
#include <vector>
#include <cmath>
#include <unordered_map>
#include <set>
#include <memory>
#include "../../../shared/Vector2.hpp"
#include "../../../shared/Angle.hpp"

using namespace nanobind::literals;

struct PairHash
{
    size_t operator()(const std::pair<int, int> &pair) const noexcept
    {
        return std::hash<int>{}(pair.first) ^ (std::hash<int>{}(pair.second) << 1);
    }
};

const int CELL_SIZE = 60;
const Vector2 ZERO_VECTOR = Vector2(0.0f, 0.0f);
std::unordered_map<std::pair<int, int>, std::vector<int>, PairHash> collisionGrid;
bool checkGridForCleanup = false;

struct CollisionMask
{
    int id;
    std::shared_ptr<Vector2> position;
    std::shared_ptr<Vector2> size;
    std::shared_ptr<Angle> rotation;
    std::vector<Vector2> vertices;
    std::vector<Vector2> axes;
    std::vector<std::pair<int, int>> occupiedCells;

    void removeFromGrid()
    {
        for (const auto &cellPair : occupiedCells)
        {
            auto &instances = collisionGrid[cellPair];
            auto it = std::find(instances.begin(), instances.end(), id);

            if (it != instances.end())
            {
                *it = instances.back();
                instances.pop_back();
            }
        }

        occupiedCells.clear();
        checkGridForCleanup = true;
    }

    void recompute()
    {
        // Its possible for size to be zero if the instance was just created
        if (size->x <= 0.0f || size->y <= 0.0f)
        {
            axes.clear();
            vertices.clear();
            return;
        }

        std::vector<Vector2> localVertices = {Vector2{0, 0}, Vector2{size->x, 0}, Vector2{size->x, size->y}, Vector2{0, size->y}};
        float cosRotation = std::cos(rotation->radians);
        float sinRotation = std::sin(rotation->radians);

        vertices.clear();

        for (auto &localVertex : localVertices)
            vertices.push_back(Vector2{position->x + localVertex.x * cosRotation - localVertex.y * sinRotation, position->y + localVertex.x * sinRotation + localVertex.y * cosRotation});

        axes.clear();

        for (size_t index = 0; index < vertices.size(); index++)
        {
            Vector2 &vertex1 = vertices[index];
            Vector2 &vertex2 = vertices[(index + 1) % vertices.size()];
            float axisX = vertex2.x - vertex1.x;
            float axisY = vertex2.y - vertex1.y;
            float axisLength = std::hypot(axisX, axisY);

            if (axisLength == 0)
                continue;

            axisX /= axisLength;
            axisY /= axisLength;
            axes.push_back(Vector2{axisY, -axisX});
        }

        removeFromGrid();

        // Determine its placement in the grid
        int cellX = static_cast<int>(std::floor(position->x / CELL_SIZE));
        int cellY = static_cast<int>(std::floor(position->y / CELL_SIZE));
        int maxX = static_cast<int>(std::floor((position->x + size->x) / CELL_SIZE));
        int maxY = static_cast<int>(std::floor((position->y + size->y) / CELL_SIZE));

        for (int x = cellX; x <= maxX; ++x)
            for (int y = cellY; y <= maxY; ++y)
            {
                std::pair<int, int> cell = {x, y};
                occupiedCells.push_back(cell);
                collisionGrid[cell].push_back(id);
            }
    }
};

std::unordered_map<int, CollisionMask *> collisionMasks;

void createCollisionMask(int id, std::shared_ptr<Vector2> size, std::shared_ptr<Vector2> position, std::shared_ptr<Angle> rotation)
{
    CollisionMask *collisionMask = new CollisionMask();
    collisionMask->id = id;
    collisionMask->size = size;
    collisionMask->position = position;
    collisionMask->rotation = rotation;
    collisionMask->recompute();
    collisionMasks[id] = collisionMask;
}

void destroyCollisionMask(int id)
{
    collisionMasks[id]->removeFromGrid();
    delete collisionMasks[id];
    collisionMasks.erase(id);
}

std::pair<float, float> projectPolygon(const Vector2 &axis, const std::vector<Vector2> &vertices)
{
    int length = vertices.size();
    std::vector<float> dots(length, 0.0f);

    for (int index = 0; index < length; ++index)
    {
        const Vector2 &vertex = vertices[index];
        dots[index] = vertex.dot(axis);
    }

    float min = dots[0];
    float max = dots[0];

    for (int index = 1; index < length; ++index)
    {
        if (dots[index] < min)
            min = dots[index];

        if (dots[index] > max)
            max = dots[index];
    }

    return {min, max};
}

void computeCollisionData(nanobind::list *collisions, std::pair<int, int> pair, const CollisionMask *instance1Mask, const CollisionMask *instance2Mask)
{
    std::vector<Vector2> axes;

    for (const auto &axis : instance1Mask->axes)
        axes.push_back(axis);

    for (const auto &axis : instance2Mask->axes)
        axes.push_back(axis);

    if (axes.empty())
        return;

    float minOverlap = 1e9;
    Vector2 smallestAxis;

    for (const auto &axis : axes)
    {
        auto [projection1X, projection1Y] = projectPolygon(axis, instance1Mask->vertices);
        auto [projection2X, projection2Y] = projectPolygon(axis, instance2Mask->vertices);

        if (!(projection1X <= projection2Y && projection2X <= projection1Y))
            return;

        float overlap = std::min(projection1Y, projection2Y) - std::max(projection1X, projection2X);

        if (overlap < minOverlap)
        {
            minOverlap = overlap;
            smallestAxis = axis.copy();
        }
    }

    Vector2 distance = *instance2Mask->position - *instance1Mask->position;

    if (distance.dot(smallestAxis) < 0)
    {
        smallestAxis.x = -smallestAxis.x;
        smallestAxis.y = -smallestAxis.y;
    }

    Vector2 normal = smallestAxis;
    Vector2 contactPoint = *instance1Mask->position + smallestAxis * (minOverlap / 2);

    collisions->append(nanobind::make_tuple(pair, minOverlap, normal, contactPoint));
}

nanobind::list checkCollisions(const nanobind::dict validCollisionMasks, const nanobind::list updatedCollisionMasks)
{
    std::set<std::pair<int, int>> checkedPairs;
    nanobind::list collisions;

    if (checkGridForCleanup)
    {
        checkGridForCleanup = false;

        for (auto it = collisionGrid.begin(); it != collisionGrid.end();)
        {
            if (it->second.empty())
            {
                it = collisionGrid.erase(it);
            }
            else
            {
                ++it;
            }
        }
    }

    for (auto data : updatedCollisionMasks)
    {
        int activeInstanceID = nanobind::cast<int>(data);

        auto it = collisionMasks.find(activeInstanceID);

        if (it == collisionMasks.end())
            continue;

        CollisionMask *activeCollisionMask = it->second;
        activeCollisionMask->recompute();

        for (const auto &cellCoord : activeCollisionMask->occupiedCells)
        {
            if (collisionGrid.find(cellCoord) == collisionGrid.end())
                continue;

            auto &neighbors = collisionGrid[cellCoord];

            for (int neighborInstanceID : neighbors)
            {
                if (activeInstanceID == neighborInstanceID || !validCollisionMasks.contains(neighborInstanceID))
                    continue;

                int id1 = std::min(activeInstanceID, neighborInstanceID);
                int id2 = std::max(activeInstanceID, neighborInstanceID);
                std::pair<int, int> pair = {id1, id2};

                if (checkedPairs.count(pair))
                    continue;

                checkedPairs.insert(pair);

                CollisionMask *neighborCollisionMask = collisionMasks[neighborInstanceID];
                computeCollisionData(&collisions, pair, activeCollisionMask, neighborCollisionMask);
            }
        }
    }

    return collisions;
}

NB_MODULE(CollisionSolver, m)
{
    m.def("create_collision_mask", &createCollisionMask, "id"_a, "size"_a, "position"_a, "rotation"_a);
    m.def("destroy_collision_mask", &destroyCollisionMask, "id"_a);
    m.def("check_collisions", &checkCollisions, "valid_collision_masks"_a, "updated_collision_masks"_a);
}