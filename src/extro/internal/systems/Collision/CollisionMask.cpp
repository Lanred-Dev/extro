#include <nanobind/nanobind.h>
#include <vector>
#include <cmath>

using namespace nanobind::literals;

float dot(float ax, float ay, float bx, float by)
{
    return ax * bx + ay * by;
}

std::tuple<float, float> projectPolygon(nanobind::tuple axis, nanobind::list vertices)
{
    int length = vertices.size();
    std::vector<float> dots(length, 0.0f);

    for (int index = 0; index < length; ++index)
    {
        nanobind::tuple vertex = vertices[index];
        dots[index] = dot(nanobind::cast<float>(vertex[0]), nanobind::cast<float>(vertex[1]), nanobind::cast<float>(axis[0]), nanobind::cast<float>(axis[1]));
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

    return std::make_tuple(min, max);
}

nanobind::list computeVertices(float sizeX, float sizeY, float positionX, float positionY, float rotation)
{
    rotation = rotation * (atan(1.0) * 4) / 180;
    float halfWidth = sizeX / 2;
    float halfHeight = sizeY / 2;
    std::vector<std::tuple<float, float>> localVertices = {std::make_tuple(-halfWidth, -halfHeight), std::make_tuple(halfWidth, -halfHeight), std::make_tuple(halfWidth, halfHeight), std::make_tuple(-halfWidth, halfHeight)};
    float cos_rotation = std::cos(rotation);
    float sin_rotation = std::sin(rotation);

    nanobind::list vertices = nanobind::list();

    for (int index = 0; index < 4; index++)
    {
        float vertex_x = std::get<0>(localVertices[index]);
        float vertex_y = std::get<1>(localVertices[index]);
        vertices.append(nanobind::make_tuple(positionX + vertex_x * cos_rotation - vertex_y * sin_rotation, positionY + vertex_x * sin_rotation + vertex_y * cos_rotation));
    }

    return vertices;
}

nanobind::list computeAxes(nanobind::list vertices)
{
    nanobind::list axes = nanobind::list();

    for (size_t index = 0; index < vertices.size(); index++)
    {
        nanobind::tuple vertex1 = vertices[index];
        nanobind::tuple vertex2 = vertices[(index + 1) % vertices.size()];
        float axisX = nanobind::cast<float>(vertex2[0] - vertex1[0]);
        float axisY = nanobind::cast<float>(vertex2[1] - vertex1[1]);
        float axisLength = std::hypot(axisX, axisY);

        if (axisLength == 0)
            continue;

        axisX /= axisLength;
        axisY /= axisLength;
        axes.append(nanobind::make_tuple(axisY, -axisX));
    }

    return axes;
}

nanobind::tuple doesCollide(nanobind::list instance1Vertices, nanobind::list instance1Axes, nanobind::list instance1Position, nanobind::list instance2Vertices, nanobind::list instance2Axes, nanobind::list instance2Position)
{
    // Combine the axes from both polygons
    std::vector<nanobind::tuple> axes;

    for (size_t index = 0; index < instance1Axes.size(); ++index)
        axes.push_back(instance1Axes[index]);
    for (size_t index = 0; index < instance2Axes.size(); ++index)
        axes.push_back(instance2Axes[index]);

    float minOverlap = 1e9;
    nanobind::tuple smallestAxis = nanobind::make_tuple(0.0, 0.0);

    for (int index = 0; index < axes.size(); index++)
    {
        nanobind::tuple axis = axes[index];
        auto [projection1X, projection1Y] = projectPolygon(axis, instance1Vertices);
        auto [projection2X, projection2Y] = projectPolygon(axis, instance2Vertices);

        if (!(projection1X <= projection2Y && projection2X <= projection1Y))
        {
            nanobind::tuple emptyTuple = nanobind::make_tuple(0.0, 0.0);
            return nanobind::make_tuple(false, emptyTuple, 0.0, emptyTuple, emptyTuple);
        }

        float overlap = std::min(projection1Y, projection2Y) - std::max(projection1X, projection2X);

        if (overlap < minOverlap)
        {
            minOverlap = overlap;
            smallestAxis = axis;
        }
    }

    float smallestAxisX = nanobind::cast<float>(smallestAxis[0]);
    float smallestAxisY = nanobind::cast<float>(smallestAxis[1]);
    float distanceX = nanobind::cast<float>(instance2Position[0] - instance1Position[0]);
    float distanceY = nanobind::cast<float>(instance2Position[1] - instance1Position[1]);

    if (dot(distanceX, distanceY, smallestAxisX, smallestAxisY) < 0)
    {
        smallestAxisX = -smallestAxisX;
        smallestAxisY = -smallestAxisY;
    }

    float normalLength = std::sqrt(smallestAxisX * smallestAxisX + smallestAxisY * smallestAxisY);
    nanobind::tuple collisionNormal = nanobind::make_tuple(smallestAxisX / normalLength, smallestAxisY / normalLength);

    float contactX = nanobind::cast<float>(instance1Position[0]) + smallestAxisX * (minOverlap / 2);
    float contactY = nanobind::cast<float>(instance1Position[1]) + smallestAxisY * (minOverlap / 2);
    nanobind::tuple contactPoint = nanobind::make_tuple(contactX, contactY);

    return nanobind::make_tuple(true, nanobind::make_tuple(smallestAxisX, smallestAxisY), minOverlap, collisionNormal, contactPoint);
}

NB_MODULE(CollisionMask, m)
{
    m.def("compute_vertices", &computeVertices, "size_x"_a, "size_y"_a, "position_x"_a, "position_y"_a, "rotation"_a);
    m.def("compute_axes", &computeAxes, "vertices"_a);
    m.def("does_collide", &doesCollide, "instance1_vertices"_a, "instance1_axes"_a, "instance1_position"_a, "instance2_vertices"_a, "instance2_axes"_a, "instance2_position"_a);
}