#include <nanobind/nanobind.h>
#include <vector>
#include <cmath>
#include "../../../shared/Vector2.hpp"

using namespace nanobind::literals;

const float IMPULSE_EPSILON = 0.01f;
const float MOMENT_OF_INERTIA_CONSTANT = 1.0f / 12.0f;
float IMPULSE_SCALER = 1.7f;
const Vector2 ZERO_VECTOR = Vector2(0.0f, 0.0f);
const float DEGREES_TO_RAD = (atan(1.0f) * 4.0f) / 180.0f;
const float RAD_TO_DEGREES = 1.0f / DEGREES_TO_RAD;

nanobind::tuple solveImpulse(Vector2 normal, Vector2 contactPoint, float restitution, float totalInverseMass, nanobind::list instance1Bounding, Vector2 instance1Velocity, bool isInstance1Dynamic, float instance1RotationalVelocity, float instance1Mass, nanobind::list instance2Bounding, Vector2 instance2Velocity, bool isInstance2Dynamic, float instance2RotationalVelocity, float instance2Mass)
{
    float instance1RotationalVelocityRad = instance1RotationalVelocity * DEGREES_TO_RAD;
    float instance2RotationalVelocityRad = instance2RotationalVelocity * DEGREES_TO_RAD;
    float instance1Width = nanobind::cast<float>(instance1Bounding[2]);
    float instance1Height = nanobind::cast<float>(instance1Bounding[3]);
    float instance2Width = nanobind::cast<float>(instance2Bounding[2]);
    float instance2Height = nanobind::cast<float>(instance2Bounding[3]);

    float instance1LevelArmX = contactPoint.x - (nanobind::cast<float>(instance1Bounding[0]) + instance1Width / 2);
    float instance1LevelArmY = contactPoint.y - (nanobind::cast<float>(instance1Bounding[1]) + instance1Height / 2);
    float instance2LevelArmX = contactPoint.x - (nanobind::cast<float>(instance2Bounding[0]) + instance2Width / 2);
    float instance2LevelArmY = contactPoint.y - (nanobind::cast<float>(instance2Bounding[1]) + instance2Height / 2);

    float relativeVelocityX = (instance2Velocity.x + (-instance2LevelArmY * instance2RotationalVelocityRad)) - (instance1Velocity.x + (-instance1LevelArmY * instance1RotationalVelocityRad));
    float relativeVelocityY = (instance2Velocity.y + (instance2LevelArmX * instance2RotationalVelocityRad)) - (instance1Velocity.y + (instance1LevelArmX * instance1RotationalVelocityRad));

    float velocityAlongNormal = relativeVelocityX * normal.x + relativeVelocityY * normal.y;

    if (velocityAlongNormal > -IMPULSE_EPSILON)
        return nanobind::make_tuple(false, ZERO_VECTOR, 0, ZERO_VECTOR, 0);

    float instance1Inertia = MOMENT_OF_INERTIA_CONSTANT * instance1Mass * (instance1Width * instance1Width + instance1Height * instance1Height);
    float instance2Inertia = MOMENT_OF_INERTIA_CONSTANT * instance2Mass * (instance2Width * instance2Width + instance2Height * instance2Height);
    float instance1AngularImpulse = instance1LevelArmX * normal.y - instance1LevelArmY * normal.x;
    float instance2AngularImpulse = instance2LevelArmX * normal.y - instance2LevelArmY * normal.x;
    float impulseMagnitude = ((-(1 + restitution) * velocityAlongNormal) / (totalInverseMass + (instance1AngularImpulse * instance1AngularImpulse) / instance1Inertia + (instance2AngularImpulse * instance2AngularImpulse) / instance2Inertia)) * IMPULSE_SCALER;

    Vector2 impulse = normal * impulseMagnitude;

    if (isInstance1Dynamic)
    {
        instance1Velocity.x -= impulse.x / instance1Mass;
        instance1Velocity.y -= impulse.y / instance1Mass;
        instance1RotationalVelocityRad -= (impulseMagnitude * instance1AngularImpulse) / instance1Inertia;
    }

    if (isInstance2Dynamic)
    {
        instance2Velocity.x += impulse.x / instance2Mass;
        instance2Velocity.y += impulse.y / instance2Mass;
        instance2RotationalVelocityRad += (impulseMagnitude * instance2AngularImpulse) / instance2Inertia;
    }

    return nanobind::make_tuple(true, instance1Velocity, instance1RotationalVelocityRad * RAD_TO_DEGREES, instance2Velocity, instance2RotationalVelocityRad * RAD_TO_DEGREES);
}

void setImpulseScaler(float scaler)
{
    IMPULSE_SCALER = scaler;
}

NB_MODULE(PhysicsSolver, m)
{
    m.def("solve_impulse", &solveImpulse, "normal"_a, "contact_point"_a, "restitution"_a, "total_inverse_mass"_a, "instance1_bounding"_a, "instance1_velocity"_a, "is_instance1_dynamic"_a, "instance1_rotational_velocity"_a, "instance1_mass"_a, "instance2_bounding"_a, "instance2_velocity"_a, "is_instance2_dynamic"_a, "instance2_rotational_velocity"_a, "instance2_mass"_a);
    m.def("set_impulse_scaler", &setImpulseScaler, "scaler"_a);
}