#include <nanobind/nanobind.h>

#include <vector>

#include <cmath>

using namespace nanobind::literals;

const float IMPULSE_EPSILON = 0.001f;

const float MOMENT_OF_INERTIA_CONSTANT = 1.0f / 12.0f;

const float IMPULSE_SCALER = 1.5f;

nanobind::tuple solveImpulse(nanobind::tuple normal, nanobind::tuple contactPoint, float restitution, float totalInverseMass, nanobind::list instance1Bounding, nanobind::tuple instance1Velocity, bool isInstance1Dynamic, float instance1RotationalVelocity, float instance1Mass, nanobind::list instance2Bounding, nanobind::tuple instance2Velocity, bool isInstance2Dynamic, float instance2RotationalVelocity, float instance2Mass)
{
    float contactX = nanobind::cast<float>(contactPoint[0]);
    float contactY = nanobind::cast<float>(contactPoint[1]);

    float instance1Width = nanobind::cast<float>(instance1Bounding[2]);
    float instance1Height = nanobind::cast<float>(instance1Bounding[3]);
    float instance2Width = nanobind::cast<float>(instance2Bounding[2]);
    float instance2Height = nanobind::cast<float>(instance2Bounding[3]);

    float instance1LevelArmX = contactX - (nanobind::cast<float>(instance1Bounding[0]) + instance1Width / 2);
    float instance1LevelArmY = contactY - (nanobind::cast<float>(instance1Bounding[1]) + instance1Height / 2);
    float instance2LevelArmX = contactX - (nanobind::cast<float>(instance2Bounding[0]) + instance2Width / 2);
    float instance2LevelArmY = contactY - (nanobind::cast<float>(instance2Bounding[1]) + instance2Height / 2);

    float instance1VelocityX = nanobind::cast<float>(instance1Velocity[0]);
    float instance1VelocityY = nanobind::cast<float>(instance1Velocity[1]);
    float instance2VelocityX = nanobind::cast<float>(instance2Velocity[0]);
    float instance2VelocityY = nanobind::cast<float>(instance2Velocity[1]);

    float relativeVelocityX = (instance2VelocityX + (-instance2LevelArmY * instance2RotationalVelocity)) - (instance1VelocityX + (-instance1LevelArmY * instance1RotationalVelocity));
    float relativeVelocityY = (instance2VelocityY + (instance2LevelArmX * instance2RotationalVelocity)) - (instance1VelocityY + (instance1LevelArmX * instance1RotationalVelocity));

    float normalX = nanobind::cast<float>(normal[0]);
    float normalY = nanobind::cast<float>(normal[1]);
    float velocityAlongNormal = relativeVelocityX * normalX + relativeVelocityY * normalY;

    if (velocityAlongNormal > -IMPULSE_EPSILON)
        return nanobind::make_tuple(false, 0, 0, 0, 0, 0, 0);

    float instance1Inertia = MOMENT_OF_INERTIA_CONSTANT * instance1Mass * (instance1Width * instance1Width + instance1Height * instance1Height);
    float instance2Inertia = MOMENT_OF_INERTIA_CONSTANT * instance2Mass * (instance2Width * instance2Width + instance2Height * instance2Height);
    float instance1AngularImpulse = instance1LevelArmX * normalY - instance1LevelArmY * normalX;
    float instance2AngularImpulse = instance2LevelArmX * normalY - instance2LevelArmY * normalX;
    float impulseMagnitude = ((-(1 + restitution) * velocityAlongNormal) / (totalInverseMass + (instance1AngularImpulse * instance1AngularImpulse) / instance1Inertia + (instance2AngularImpulse * instance2AngularImpulse) / instance2Inertia)) * IMPULSE_SCALER;

    float impulseX = normalX * impulseMagnitude;
    float impulseY = normalY * impulseMagnitude;

    if (isInstance1Dynamic)
    {
        instance1VelocityX -= impulseX / instance1Mass;
        instance1VelocityY -= impulseY / instance1Mass;
        instance1RotationalVelocity -= (impulseMagnitude * instance1AngularImpulse) / instance1Inertia;
    }

    if (isInstance2Dynamic)
    {
        instance2VelocityX += impulseX / instance2Mass;
        instance2VelocityY += impulseY / instance2Mass;
        instance2RotationalVelocity += (impulseMagnitude * instance2AngularImpulse) / instance2Inertia;
    }

    return nanobind::make_tuple(true, instance1VelocityX, instance1VelocityY, instance1RotationalVelocity, instance2VelocityX, instance2VelocityY, instance2RotationalVelocity);
}

NB_MODULE(PhysicsSolver, m)
{
    m.def("solve_impulse", &solveImpulse, "normal"_a, "contact_point"_a, "restitution"_a, "total_inverse_mass"_a, "instance1_bounding"_a, "instance1_velocity"_a, "is_instance1_dynamic"_a, "instance1_rotational_velocity"_a, "instance1_mass"_a, "instance2_bounding"_a, "instance2_velocity"_a, "is_instance2_dynamic"_a, "instance2_rotational_velocity"_a, "instance2_mass"_a);
}