#include <nanobind/nanobind.h>
#include <nanobind/stl/pair.h>
#include <nanobind/stl/vector.h>
#include <vector>
#include <cmath>
#include <set>
#include <unordered_map>

using namespace nanobind::literals;

struct SimpleVector2
{
    float x;
    float y;
};

struct CollisionMask
{
    SimpleVector2 position;
    SimpleVector2 size;
    float rotation;
    std::vector<SimpleVector2> vertices;
    std::vector<SimpleVector2> axes;
};

struct PairHash
{
    size_t operator()(const std::pair<int, int> &pair) const noexcept
    {
        return std::hash<int>{}(pair.first) ^ (std::hash<int>{}(pair.second) << 1);
    }
};

const int CELL_SIZE = 60;

std::unordered_map<int, CollisionMask> collisionMasks;

float dot(const float ax, const float ay, const float bx, const float by)
{
    return ax * bx + ay * by;
}

std::pair<float, float> projectPolygon(SimpleVector2 axis, std::vector<SimpleVector2> vertices)
{
    int length = vertices.size();
    std::vector<float> dots(length, 0.0f);

    for (int index = 0; index < length; ++index)
    {
        SimpleVector2 &vertex = vertices[index];
        dots[index] = dot(vertex.x, vertex.y, axis.x, axis.y);
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

void recomputeCollisionMask(int instanceID, float width, float height, float positionX, float positionY, float rotation)
{
    rotation = rotation * (atan(1.0) * 4) / 180;
    float halfWidth = width / 2;
    float halfHeight = height / 2;
    std::vector<SimpleVector2> localVertices = {SimpleVector2{-halfWidth, -halfHeight}, SimpleVector2{halfWidth, -halfHeight}, SimpleVector2{halfWidth, halfHeight}, SimpleVector2{-halfWidth, halfHeight}};
    float cos_rotation = std::cos(rotation);
    float sin_rotation = std::sin(rotation);

    std::vector<SimpleVector2> vertices;

    for (int index = 0; index < 4; index++)
    {
        SimpleVector2 &localVertex = localVertices[index];
        vertices.push_back(SimpleVector2{positionX + localVertex.x * cos_rotation - localVertex.y * sin_rotation, positionY + localVertex.x * sin_rotation + localVertex.y * cos_rotation});
    }

    std::vector<SimpleVector2> axes;

    for (size_t index = 0; index < vertices.size(); index++)
    {
        SimpleVector2 &vertex1 = vertices[index];
        SimpleVector2 &vertex2 = vertices[(index + 1) % vertices.size()];
        float axisX = vertex2.x - vertex1.x;
        float axisY = vertex2.y - vertex1.y;
        float axisLength = std::hypot(axisX, axisY);

        if (axisLength == 0)
            continue;

        axisX /= axisLength;
        axisY /= axisLength;
        axes.push_back(SimpleVector2{axisY, -axisX});
    }

    collisionMasks[instanceID] = CollisionMask{SimpleVector2{positionX, positionY}, SimpleVector2{width, height}, rotation, vertices, axes};
}

std::tuple<bool, float, std::pair<float, float>, std::pair<float, float>> doesCollide(int instance1ID, int instance2ID)
{
    CollisionMask &instance1Mask = collisionMasks[instance1ID];
    CollisionMask &instance2Mask = collisionMasks[instance2ID];

    // Combine the axes from both polygons
    std::vector<SimpleVector2> axes;

    for (size_t index = 0; index < instance1Mask.axes.size(); ++index)
        axes.push_back(instance1Mask.axes[index]);

    for (size_t index = 0; index < instance2Mask.axes.size(); ++index)
        axes.push_back(instance2Mask.axes[index]);

    float minOverlap = 1e9;
    SimpleVector2 smallestAxis;

    for (int index = 0; index < axes.size(); index++)
    {
        SimpleVector2 &axis = axes[index];
        auto [projection1X, projection1Y] = projectPolygon(axis, instance1Mask.vertices);
        auto [projection2X, projection2Y] = projectPolygon(axis, instance2Mask.vertices);

        if (!(projection1X <= projection2Y && projection2X <= projection1Y))
        {
            return std::make_tuple(false, 0.0f, std::make_pair(0.0f, 0.0f), std::make_pair(0.0f, 0.0f));
        }

        float overlap = std::min(projection1Y, projection2Y) - std::max(projection1X, projection2X);

        if (overlap < minOverlap)
        {
            minOverlap = overlap;
            smallestAxis = axis;
        }
    }

    float distanceX = instance2Mask.position.x - instance1Mask.position.x;
    float distanceY = instance2Mask.position.y - instance1Mask.position.y;

    if (dot(distanceX, distanceY, smallestAxis.x, smallestAxis.y) < 0)
    {
        smallestAxis.x = -smallestAxis.x;
        smallestAxis.y = -smallestAxis.y;
    }

    float normalLength = std::sqrt(smallestAxis.x * smallestAxis.x + smallestAxis.y * smallestAxis.y);
    std::pair<float, float> normal = {smallestAxis.x / normalLength, smallestAxis.y / normalLength};

    float contactX = instance1Mask.position.x + smallestAxis.x * (minOverlap / 2);
    float contactY = instance1Mask.position.y + smallestAxis.y * (minOverlap / 2);
    std::pair<float, float> contactPoint = {contactX, contactY};

    return std::make_tuple(true, minOverlap, normal, contactPoint);
}

nanobind::list checkCollisions(nanobind::list validCollisionMasks)
{
    std::set<std::pair<int, int>> checkedPairs;
    nanobind::list collisions;
    std::unordered_map<std::pair<int, int>, std::vector<int>, PairHash> grid;

    for (const auto &[id, mask] : collisionMasks)
    {
        int cellX = static_cast<int>(std::floor(mask.position.x / CELL_SIZE));
        int cellY = static_cast<int>(std::floor(mask.position.y / CELL_SIZE));
        int maxX = static_cast<int>(std::floor((mask.position.x + mask.size.x) / CELL_SIZE));
        int maxY = static_cast<int>(std::floor((mask.position.y + mask.size.y) / CELL_SIZE));

        for (int x = cellX; x <= maxX; ++x)
            for (int y = cellY; y <= maxY; ++y)
                grid[{x, y}].push_back(id);
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
    m.def("recompute_collision_mask", &recomputeCollisionMask, "instance_id"_a, "size_x"_a, "size_y"_a, "position_x"_a, "position_y"_a, "rotation"_a);
    m.def("check_collisions", &checkCollisions);
}