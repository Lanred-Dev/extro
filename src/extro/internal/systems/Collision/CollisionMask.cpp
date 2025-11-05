#include <nanobind/nanobind.h>
#include <vector>
#include <cmath>

using namespace nanobind::literals;

float dot(nanobind::tuple a, nanobind::tuple b)
{
    return nanobind::cast<float>(a[0]) * nanobind::cast<float>(b[0]) + nanobind::cast<float>(a[1]) * nanobind::cast<float>(b[1]);
}

std::tuple<float, float> projectPolygon(nanobind::tuple axis, nanobind::list vertices)
{
    int length = vertices.size();
    std::vector<float> dots(length, 0.0f);

    for (int index = 0; index < length; ++index)
    {
        dots[index] = dot(vertices[index], axis);
    }

    float min_dot = dots[0];
    float max_dot = dots[0];

    for (int index = 1; index < length; ++index)
    {
        if (dots[index] < min_dot)
        {
            min_dot = dots[index];
        }

        if (dots[index] > max_dot)
        {
            max_dot = dots[index];
        }
    }

    return std::make_tuple(min_dot, max_dot);
}

nanobind::list computeVertices(float sizeX, float sizeY, float positionX, float positionY, float rotation)
{
    rotation = rotation * (atan(1.0) * 4) / 180;
    float halfWidth = sizeX / 2;
    float halfHeight = sizeY / 2;
    std::vector<std::tuple<float, float>> local_vertices = {std::make_tuple(-halfWidth, -halfHeight), std::make_tuple(halfWidth, -halfHeight), std::make_tuple(halfWidth, halfHeight), std::make_tuple(-halfWidth, halfHeight)};
    float cos_rotation = std::cos(rotation);
    float sin_rotation = std::sin(rotation);

    nanobind::list vertices = nanobind::list();

    for (int index = 0; index < 4; index++)
    {
        float vertex_x = std::get<0>(local_vertices[index]);
        float vertex_y = std::get<1>(local_vertices[index]);
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

nanobind::tuple doesCollide(nanobind::list instance1Vertices, nanobind::list instance1Axes, nanobind::tuple instance1Position, nanobind::list instance2Vertices, nanobind::list instance2Axes, nanobind::tuple instance2Position)
{
    // Combine the axes from both polygons
    nanobind::list axes;
    for (size_t index = 0; index < instance1Axes.size(); ++index)
        axes.append(instance1Axes[index]);
    for (size_t index = 0; index < instance2Axes.size(); ++index)
        axes.append(instance2Axes[index]);

    nanobind::tuple axis;
    nanobind::tuple projection1;
    nanobind::tuple projection2;
    float overlap;
    float minOverlap = 1e9;
    nanobind::tuple smallestAxis = nanobind::make_tuple(0.0, 0.0);

    for (int index = 0; index < axes.size(); index++)
    {
        nanobind::tuple axis = axes[index];
        std::tuple<float, float> projection1 = projectPolygon(axis, instance1Vertices);
        std::tuple<float, float> projection2 = projectPolygon(axis, instance2Vertices);

        if (!(std::get<0>(projection1) <= std::get<1>(projection2) && std::get<0>(projection2) <= std::get<1>(projection1)))
        {
            nanobind::tuple emptyTuple = nanobind::make_tuple(0.0, 0.0);
            return nanobind::make_tuple(false, emptyTuple, 0.0, emptyTuple, emptyTuple);
        }

        overlap = std::min(std::get<1>(projection1), std::get<1>(projection2)) - std::max(std::get<0>(projection1), std::get<0>(projection2));

        if (overlap < minOverlap)
        {
            minOverlap = overlap;
            smallestAxis = axis;
        }
    }

    nanobind::tuple distance = nanobind::make_tuple(instance2Position[0] - instance1Position[0], instance2Position[1] - instance1Position[1]);

    if (dot(distance, smallestAxis) < 0)
        smallestAxis = nanobind::make_tuple(-nanobind::cast<float>(smallestAxis[0]), -nanobind::cast<float>(smallestAxis[1]));

    float collisionNormalX = nanobind::cast<float>(smallestAxis[0]);
    float collisionNormalY = nanobind::cast<float>(smallestAxis[1]);
    float normalLength = std::sqrt(collisionNormalX * collisionNormalX + collisionNormalY * collisionNormalY);
    collisionNormalX /= normalLength;
    collisionNormalY /= normalLength;
    nanobind::tuple collisionNormal = nanobind::make_tuple(collisionNormalX, collisionNormalY);

    float contactX = nanobind::cast<float>(instance1Position[0]) + nanobind::cast<float>(smallestAxis[0]) * (minOverlap / 2);
    float contactY = nanobind::cast<float>(instance1Position[1]) + nanobind::cast<float>(smallestAxis[1]) * (minOverlap / 2);
    nanobind::tuple contactPoint = nanobind::make_tuple(contactX, contactY);

    return nanobind::make_tuple(true, smallestAxis, minOverlap, collisionNormal, contactPoint);
}

NB_MODULE(CollisionMask, m)
{
    m.def("compute_vertices", &computeVertices, "size_x"_a, "size_y"_a, "position_x"_a, "position_y"_a, "rotation"_a);
    m.def("compute_axes", &computeAxes, "vertices"_a);
    m.def("does_collide", &doesCollide, "instance1_vertices"_a, "instance1_axes"_a, "instance1_position"_a, "instance2_vertices"_a, "instance2_axes"_a, "instance2_position"_a);
}