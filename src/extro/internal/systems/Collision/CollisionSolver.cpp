#include <nanobind/nanobind.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/vector.h>
#include <vector>
#include <cmath>
#include <unordered_map>
#include <set>
#include "../../../shared/Vector2.hpp"

using namespace nanobind::literals;

const int CELL_SIZE = 60;
const Vector2 ZERO_VECTOR = Vector2(0.0f, 0.0f);

struct CollisionMask
{
    Vector2 position;
    Vector2 size;
    float rotation;
    std::vector<Vector2> vertices;
    std::vector<Vector2> axes;

    void recompute()
    {
        float rotationRad = rotation * (atan(1.0) * 4) / 180;
        float halfWidth = size.x / 2.0f;
        float halfHeight = size.y / 2.0f;
        std::vector<Vector2> localVertices = {Vector2{-halfWidth, -halfHeight}, Vector2{halfWidth, -halfHeight}, Vector2{halfWidth, halfHeight}, Vector2{-halfWidth, halfHeight}};
        float cosRotation = std::cos(rotationRad);
        float sinRotation = std::sin(rotationRad);

        vertices.clear();

        for (auto &localVertex : localVertices)
            vertices.push_back(Vector2{position.x + localVertex.x * cosRotation - localVertex.y * sinRotation, position.y + localVertex.x * sinRotation + localVertex.y * cosRotation});

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
    }
};

std::unordered_map<int, CollisionMask *> collisionMasks;

void createCollisionMask(int instanceID, Vector2 size, Vector2 position, float rotation)
{
    CollisionMask *collisionMask = new CollisionMask();
    collisionMask->size = size;
    collisionMask->position = position;
    collisionMask->rotation = rotation;
    collisionMask->recompute();
    collisionMasks[instanceID] = collisionMask;
}

void destroyCollisionMask(int instanceID)
{
    delete collisionMasks[instanceID];
    collisionMasks.erase(instanceID);
}

struct PairHash
{
    size_t operator()(const std::pair<int, int> &pair) const noexcept
    {
        return std::hash<int>{}(pair.first) ^ (std::hash<int>{}(pair.second) << 1);
    }
};

std::pair<float, float> &projectPolygon(const Vector2 &axis, const std::vector<Vector2> &vertices)
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

    return *(new std::pair<float, float>(min, max));
}

std::tuple<bool, float, Vector2, Vector2> doesCollide(const int instance1ID, const int instance2ID)
{
    CollisionMask *instance1Mask = collisionMasks[instance1ID];
    CollisionMask *instance2Mask = collisionMasks[instance2ID];

    std::vector<Vector2 *> axes;

    for (auto &axis : instance1Mask->axes)
        axes.push_back(&axis);

    for (auto &axis : instance2Mask->axes)
        axes.push_back(&axis);

    float minOverlap = 1e9;
    Vector2 smallestAxis;

    for (const auto *axis : axes)
    {
        auto &[projection1X, projection1Y] = projectPolygon(*axis, instance1Mask->vertices);
        auto &[projection2X, projection2Y] = projectPolygon(*axis, instance2Mask->vertices);

        if (!(projection1X <= projection2Y && projection2X <= projection1Y))
        {
            return std::make_tuple(false, 0.0f, ZERO_VECTOR.copy(), ZERO_VECTOR.copy());
        }

        float overlap = std::min(projection1Y, projection2Y) - std::max(projection1X, projection2X);

        if (overlap < minOverlap)
        {
            minOverlap = overlap;
            smallestAxis = axis->copy();
        }
    }

    Vector2 distance = instance2Mask->position - instance1Mask->position;

    if (distance.dot(smallestAxis) < 0)
    {
        smallestAxis.x = -smallestAxis.x;
        smallestAxis.y = -smallestAxis.y;
    }

    float normalLength = std::sqrt(smallestAxis.x * smallestAxis.x + smallestAxis.y * smallestAxis.y);
    Vector2 normal = {smallestAxis.x / normalLength, smallestAxis.y / normalLength};

    float contactX = instance1Mask->position.x + smallestAxis.x * (minOverlap / 2);
    float contactY = instance1Mask->position.y + smallestAxis.y * (minOverlap / 2);
    Vector2 contactPoint = {contactX, contactY};

    return std::make_tuple(true, minOverlap, normal, contactPoint);
}

nanobind::list checkCollisions(const nanobind::list collisionMasksData)
{
    std::set<std::pair<int, int>> checkedPairs;
    nanobind::list collisions;
    std::unordered_map<std::pair<int, int>, std::vector<int>, PairHash> grid;

    for (const auto &data : collisionMasksData)
    {
        int instanceID = nanobind::cast<int>(data[0]);
        CollisionMask *collisionMask = collisionMasks[instanceID];

        if (nanobind::cast<bool>(data[2]))
        {
            nanobind::list transformUpdates = data[3];
            collisionMask->position.x = nanobind::cast<float>(transformUpdates[0]);
            collisionMask->position.y = nanobind::cast<float>(transformUpdates[1]);
            collisionMask->size.x = nanobind::cast<float>(transformUpdates[2]);
            collisionMask->size.y = nanobind::cast<float>(transformUpdates[3]);
            collisionMask->rotation = nanobind::cast<float>(transformUpdates[4]);
            collisionMask->recompute();
        }

        if (nanobind::cast<bool>(data[1]) == false)
            continue;

        int cellX = static_cast<int>(std::floor(collisionMask->position.x / CELL_SIZE));
        int cellY = static_cast<int>(std::floor(collisionMask->position.y / CELL_SIZE));
        int maxX = static_cast<int>(std::floor((collisionMask->position.x + collisionMask->size.x) / CELL_SIZE));
        int maxY = static_cast<int>(std::floor((collisionMask->position.y + collisionMask->size.y) / CELL_SIZE));

        for (int x = cellX; x <= maxX; ++x)
            for (int y = cellY; y <= maxY; ++y)
                grid[{x, y}].push_back(instanceID);
    }

    for (auto &cell : grid)
    {
        std::vector<int> &instances = cell.second;

        for (size_t index1 = 0; index1 < instances.size(); ++index1)
        {
            for (size_t index2 = index1 + 1; index2 < instances.size(); ++index2)
            {
                int instance1ID = instances[index1];
                int instance2ID = instances[index2];
                std::pair<int, int> collision = {instance1ID, instance2ID};

                if (checkedPairs.find(collision) != checkedPairs.end())
                    continue;

                checkedPairs.insert(collision);
                auto [collides, penetration, normal, contactPoint] = doesCollide(instance1ID, instance2ID);

                if (!collides)
                    continue;

                collisions.append(nanobind::make_tuple(collision, penetration, normal, contactPoint));
            }
        }
    }

    return collisions;
}

NB_MODULE(CollisionSolver, m)
{
    m.def("create_collision_mask", &createCollisionMask, "instance_id"_a, "size"_a, "position"_a, "rotation"_a);
    m.def("destroy_collision_mask", &destroyCollisionMask, "instance_id"_a);
    m.def("check_collisions", &checkCollisions);
}