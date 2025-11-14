'use client'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BookOpen, Play } from 'lucide-react'

interface Exercise {
  id: number
  title: string
  equation: string
  type: string
  difficulty: 'Básico' | 'Intermedio' | 'Avanzado'
  description: string
}

const exercises: Exercise[] = [
  {
    id: 1,
    title: 'Crecimiento exponencial',
    equation: 'dy/dx = y',
    type: 'separable',
    difficulty: 'Básico',
    description: 'Modelo clásico de crecimiento exponencial'
  },
  {
    id: 2,
    title: 'Variables separables con producto',
    equation: 'dy/dx = x*y',
    type: 'separable',
    difficulty: 'Básico',
    description: 'Ecuación separable básica con producto de variables'
  },
  {
    id: 3,
    title: 'Separable con funciones trigonométricas',
    equation: 'dy/dx = y^2*sin(x)',
    type: 'separable',
    difficulty: 'Intermedio',
    description: 'Incluye funciones trigonométricas y potencias'
  },
  {
    id: 4,
    title: 'Lineal de primer orden simple',
    equation: 'dy/dx + 2*y = 4*x',
    type: 'linear',
    difficulty: 'Básico',
    description: 'Ecuación lineal con coeficientes constantes'
  },
  {
    id: 5,
    title: 'Lineal con función exponencial',
    equation: 'dy/dx - y = exp(x)',
    type: 'linear',
    difficulty: 'Intermedio',
    description: 'Ecuación lineal con término no homogéneo exponencial'
  },
  {
    id: 6,
    title: 'Lineal con coeficiente variable',
    equation: 'dy/dx + y/x = x^2',
    type: 'linear',
    difficulty: 'Intermedio',
    description: 'Coeficiente P(x) variable y término Q(x) polinomial'
  },
  {
    id: 7,
    title: 'Homogénea básica',
    equation: 'dy/dx = (x+y)/x',
    type: 'homogeneous',
    difficulty: 'Básico',
    description: 'Ecuación homogénea de grado 1'
  },
  {
    id: 8,
    title: 'Homogénea con suma de cuadrados',
    equation: 'dy/dx = (x^2+y^2)/(x*y)',
    type: 'homogeneous',
    difficulty: 'Intermedio',
    description: 'Ecuación homogénea con términos cuadráticos'
  },
  {
    id: 9,
    title: 'Exacta simple',
    equation: '(2*x+y)dx + (x+2*y)dy = 0',
    type: 'exact',
    difficulty: 'Básico',
    description: 'Ecuación exacta con términos lineales'
  },
  {
    id: 10,
    title: 'Bernoulli cuadrática',
    equation: 'dy/dx + y = y^2*x',
    type: 'bernoulli',
    difficulty: 'Intermedio',
    description: 'Ecuación de Bernoulli con n=2'
  },
  {
    id: 11,
    title: 'Bernoulli cúbica',
    equation: 'dy/dx - 2*y/x = x^2*y^3',
    type: 'bernoulli',
    difficulty: 'Avanzado',
    description: 'Ecuación de Bernoulli con n=3 y coeficientes variables'
  },
  {
    id: 12,
    title: 'Circuito RC',
    equation: 'dy/dx + 3*y = sin(x)',
    type: 'linear',
    difficulty: 'Intermedio',
    description: 'Modelo de circuito RC con entrada sinusoidal'
  }
]

interface ExampleExercisesProps {
  onSelectExercise: (equation: string, type: string) => void
}

export function ExampleExercises({ onSelectExercise }: ExampleExercisesProps) {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Básico':
        return 'bg-green-500/10 text-green-700 dark:text-green-400 border-green-500/20'
      case 'Intermedio':
        return 'bg-yellow-500/10 text-yellow-700 dark:text-yellow-400 border-yellow-500/20'
      case 'Avanzado':
        return 'bg-red-500/10 text-red-700 dark:text-red-400 border-red-500/20'
      default:
        return 'bg-muted text-muted-foreground'
    }
  }

  return (
    <Card className="border-2 shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-primary" />
          Ejercicios de Ejemplo
        </CardTitle>
        <CardDescription>
          Selecciona un ejercicio para probar el solucionador
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
          {exercises.map((exercise) => (
            <div
              key={exercise.id}
              className="group p-4 rounded-lg border-2 hover:border-primary/50 transition-all hover:shadow-md bg-card"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-2 flex-wrap">
                    <h3 className="font-semibold text-sm">{exercise.title}</h3>
                    <span
                      className={`text-xs px-2 py-1 rounded-full border ${getDifficultyColor(
                        exercise.difficulty
                      )}`}
                    >
                      {exercise.difficulty}
                    </span>
                  </div>
                  <code className="text-xs font-mono bg-muted px-2 py-1 rounded block">
                    {exercise.equation}
                  </code>
                  <p className="text-xs text-muted-foreground">
                    {exercise.description}
                  </p>
                </div>
                <Button
                  size="sm"
                  variant="ghost"
                  className="shrink-0"
                  onClick={() => onSelectExercise(exercise.equation, exercise.type)}
                >
                  <Play className="w-4 h-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
