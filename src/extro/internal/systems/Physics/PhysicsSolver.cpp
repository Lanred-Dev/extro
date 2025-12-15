#include <nanobind/nanobind.h>
#include <nanobind/stl/shared_ptr.h>
#include <vector>
#include <cmath>
#include <unordered_map>
#include <memory>
#include "../../../shared/Vector2.hpp"
#include "../../../shared/Angle.hpp"

using namespace nanobind::literals;

const float IMPULSE_EPSILON = 0.01f;
const float MOMENT_OF_INERTIA_CONSTANT = 1.0f / 12.0f;
float IMPULSE_SCALER = 1.0f;
const float PENETRATION_CORRECTION = 1.0f;
const float PENETRATION_SLOP = 0.05f;
const Vector2 ZERO_VECTOR = Vector2(0.0f, 0.0f);

struct PhysicsBody
{
    int id;
    std::shared_ptr<Vector2> position;
    std::shared_ptr<Vector2> size;
    std::shared_ptr<Angle> rotation;
    std::shared_ptr<Vector2> velocity;
    std::shared_ptr<Angle> angularVelocity;
    float mass;
    float inverseMass;
    float restitution;
    float inertia;
    float inverseInertia;
    bool isDynamic;

    void recompute()
    {
        if (mass <= 0.0f || !isDynamic)
        {
            inverseMass = 0.0f;
            inertia = 0.0f;
            inverseInertia = 0.0f;
        }
        else
        {
            inertia = MOMENT_OF_INERTIA_CONSTANT * mass * size->dot(*size);
            inverseInertia = 1.0f / inertia;
        }
    }
};

std::unordered_map<int, PhysicsBody *> physicsBodies;

void createPhysicsBody(int id, std::shared_ptr<Vector2> size, std::shared_ptr<Vector2> position, std::shared_ptr<Angle> rotation, std::shared_ptr<Vector2> velocity, std::shared_ptr<Angle> angularVelocity)
{
    PhysicsBody *physicsBody = new PhysicsBody();
    physicsBody->id = id;
    physicsBody->size = size;
    physicsBody->position = position;
    physicsBody->rotation = rotation;
    physicsBody->velocity = velocity;
    physicsBody->angularVelocity = angularVelocity;
    physicsBody->mass = 1.0f;
    physicsBody->inverseMass = 1.0f;
    physicsBody->restitution = 0.2f;
    physicsBody->isDynamic = true;
    physicsBody->recompute();
    physicsBodies[id] = physicsBody;
}

void destroyPhysicsBody(int id)
{
    delete physicsBodies[id];
    physicsBodies.erase(id);
}

void solveImpulse(Vector2 *normal, Vector2 *contactPoint, PhysicsBody *instance1PhysicsBody, PhysicsBody *instance2PhysicsBody)
{
    Vector2 instance1LevelArm = *contactPoint - (*instance1PhysicsBody->position + *instance1PhysicsBody->size / 2);
    Vector2 instance2LevelArm = *contactPoint - (*instance2PhysicsBody->position + *instance2PhysicsBody->size / 2);

    Vector2 relativeVelocity(
        (instance2PhysicsBody->velocity->x + (-instance2LevelArm.y * instance2PhysicsBody->angularVelocity->radians)) - (instance1PhysicsBody->velocity->x + (-instance1LevelArm.y * instance1PhysicsBody->angularVelocity->radians)),
        (instance2PhysicsBody->velocity->y + (instance2LevelArm.x * instance2PhysicsBody->angularVelocity->radians)) - (instance1PhysicsBody->velocity->y + (instance1LevelArm.x * instance1PhysicsBody->angularVelocity->radians)));

    float velocityAlongNormal = relativeVelocity.dot(*normal);

    if (velocityAlongNormal > -IMPULSE_EPSILON)
        return;

    float instance1AngularImpulse = instance1LevelArm.dot(*normal);
    float instance2AngularImpulse = instance2LevelArm.dot(*normal);
    float impulseMagnitude = ((-(1 + std::min(instance1PhysicsBody->restitution, instance2PhysicsBody->restitution)) * velocityAlongNormal) / ((instance1PhysicsBody->inverseMass + instance2PhysicsBody->inverseMass) + (instance1AngularImpulse * instance1AngularImpulse) * instance1PhysicsBody->inverseInertia + (instance2AngularImpulse * instance2AngularImpulse) * instance2PhysicsBody->inverseInertia)) * IMPULSE_SCALER;

    Vector2 impulse = (*normal) * impulseMagnitude;

    if (instance1PhysicsBody->isDynamic)
    {
        instance1PhysicsBody->velocity->x -= impulse.x * instance1PhysicsBody->inverseMass;
        instance1PhysicsBody->velocity->y -= impulse.y * instance1PhysicsBody->inverseMass;
        instance1PhysicsBody->angularVelocity->setRadians(instance1PhysicsBody->angularVelocity->radians - ((impulseMagnitude * instance1AngularImpulse) * instance1PhysicsBody->inverseInertia));
    }

    if (instance2PhysicsBody->isDynamic)
    {
        instance2PhysicsBody->velocity->x += impulse.x * instance2PhysicsBody->inverseMass;
        instance2PhysicsBody->velocity->y += impulse.y * instance2PhysicsBody->inverseMass;
        instance2PhysicsBody->angularVelocity->setRadians(instance2PhysicsBody->angularVelocity->radians + ((impulseMagnitude * instance2AngularImpulse) * instance2PhysicsBody->inverseInertia));
    }
}

void step(nanobind::list physicsBodyUpdates)
{
    for (const auto &data : physicsBodyUpdates)
    {
        PhysicsBody *physicsBody = physicsBodies[nanobind::cast<int>(data[0])];
        physicsBody->mass = nanobind::cast<float>(data[1]);
        physicsBody->inverseMass = nanobind::cast<float>(data[2]);
        physicsBody->restitution = nanobind::cast<float>(data[3]);
        physicsBody->isDynamic = nanobind::cast<bool>(data[4]);
        physicsBody->recompute();
    }
}

nanobind::list resolveCollisions(nanobind::list collisions)
{
    nanobind::list updatedInstances;

    for (const auto &data : collisions)
    {
        float penetration = nanobind::cast<float>(data[1]);

        if (penetration <= PENETRATION_SLOP)
            continue;

        nanobind::tuple collisionPair = data[0];
        int instance1ID = nanobind::cast<int>(collisionPair[0]);
        int instance2ID = nanobind::cast<int>(collisionPair[1]);
        PhysicsBody *instance1PhysicsBody = physicsBodies[instance1ID];
        PhysicsBody *instance2PhysicsBody = physicsBodies[instance2ID];

        bool isInstance1Dynamic = instance1PhysicsBody->isDynamic;
        bool isInstance2Dynamic = instance2PhysicsBody->isDynamic;

        if (!isInstance1Dynamic && !isInstance2Dynamic)
            continue;

        float totalInverseMass = (instance1PhysicsBody->inverseMass + instance2PhysicsBody->inverseMass);

        if (totalInverseMass == 0)
            continue;

        Vector2 normal = nanobind::cast<Vector2>(data[2]);
        Vector2 contactPoint = nanobind::cast<Vector2>(data[3]);

        penetration *= PENETRATION_CORRECTION;
        Vector2 correction = normal * penetration;

        solveImpulse(
            &normal,
            &contactPoint,
            instance1PhysicsBody,
            instance2PhysicsBody);

        if (isInstance1Dynamic)
        {
            float massCorrection = instance1PhysicsBody->inverseMass / totalInverseMass;
            instance1PhysicsBody->position->x -= correction.x * massCorrection;
            instance1PhysicsBody->position->y -= correction.y * massCorrection;
            updatedInstances.append(instance1ID);
        }

        if (isInstance2Dynamic)
        {
            float massCorrection = instance2PhysicsBody->inverseMass / totalInverseMass;
            instance2PhysicsBody->position->x += correction.x * massCorrection;
            instance2PhysicsBody->position->y += correction.y * massCorrection;
            updatedInstances.append(instance2ID);
        }
    }

    return updatedInstances;
}

NB_MODULE(PhysicsSolver, m)
{
    m.def("create_physics_body", &createPhysicsBody, "id"_a, "size"_a, "position"_a, "rotation"_a, "velocity"_a, "angular_velocity"_a);
    m.def("destroy_physics_body", &destroyPhysicsBody, "id"_a);
    m.def("step", &step, "physics_body_updates"_a);
    m.def("resolve_collisions", &resolveCollisions, "collisions"_a);
    m.def("set_impulse_scaler", [](float scaler)
          { IMPULSE_SCALER = scaler; }, "scaler"_a);
}