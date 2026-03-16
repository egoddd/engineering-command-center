using System;

public struct Vector3
{
    public float X;
    public float Y;
    public float Z;

    public Vector3(float x, float y, float z)
    {
        X = x;
        Y = y;
        Z = z;
    }
}

public class Particle
{
    public Vector3 Position; // Stored inline as part of the Particle object
    public float Mass;       // Stored inline as part of the Particle object

    public Particle(Vector3 position, float mass)
    {
        Position = position;
        Mass = mass;
    }
}

internal class Program
{
    private static void Main()
    {
        CreateParticles();
    }

    private static void CreateParticles()
    {
        // particles variable itself is a local reference variable on the stack.
        // The array object is allocated on the heap.
        Particle[] particles = new Particle[5];

        for (int i = 0; i < particles.Length; i++)
        {
            // position is a local value-type variable.
            // As a local variable, it is typically stack-allocated for this method frame.
            Vector3 position = new Vector3(i, i * 2, i * 3);

            // particle reference variable is local to this loop body / method frame.
            // The Particle object created by 'new' is allocated on the heap.
            Particle particle = new Particle(position, i + 1.5f);

            // particles[i] stores a reference in the heap-allocated array
            // pointing to the heap-allocated Particle object.
            particles[i] = particle;
        }

        foreach (Particle particle in particles)
        {
            // particle here is a local reference variable used by the foreach loop.
            // It refers to a Particle object on the heap.
            Console.WriteLine(
                $"Position=({particle.Position.X}, {particle.Position.Y}, {particle.Position.Z}), Mass={particle.Mass}");
        }
    }
}