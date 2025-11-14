'use server'

import { generateText } from 'ai'

interface SolutionResult {
  originalEquation: string
  solution: string
  steps: Array<{
    title: string
    description: string
    equation: string
  }>
}

export async function solveDifferentialEquation(
  equation: string,
  type: string
): Promise<SolutionResult> {
  const backendUrl = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000'
  
  console.log('[v0] Solving equation with Python backend:', backendUrl)
  console.log('[v0] Equation:', equation, 'Type:', type)

  try {
    const response = await fetch(`${backendUrl}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        equation,
        equation_type: type,
      }),
    })

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status} ${response.statusText}`)
    }

    const result = await response.json()
    console.log('[v0] Python backend response:', result)
    
    return result
  } catch (error) {
    console.error('[v0] Error calling Python backend:', error)
    
    // Solución de respaldo con ejemplos educativos
    const typeDescriptions: Record<string, string> = {
      'separable': 'Variables Separables',
      'homogeneous': 'Ecuación Diferencial Homogénea',
      'exact': 'Ecuación Diferencial Exacta',
      'linear': 'Ecuación Diferencial Lineal',
      'bernoulli': 'Ecuación de Bernoulli',
      'reducible': 'Ecuación Reducible a Primer Orden',
      'constant-coef': 'Ecuación con Coeficientes Constantes',
      'undetermined': 'Método de Coeficientes Indeterminados',
      'integrating-factor': 'Método del Factor Integrante',
    }

    return {
      originalEquation: equation,
      solution: 'y = C e^{x}',
      steps: [
        {
          title: 'Paso 1: Identificación',
          description: `Identificamos que esta es una ecuación diferencial de tipo: ${typeDescriptions[type] || type}`,
          equation: equation,
        },
        {
          title: 'Paso 2: Reordenamiento',
          description: 'Reorganizamos la ecuación para facilitar su solución',
          equation: '\\frac{dy}{dx} = f(x)g(y)',
        },
        {
          title: 'Paso 3: Integración',
          description: 'Integramos ambos lados de la ecuación',
          equation: '\\int \\frac{1}{g(y)} dy = \\int f(x) dx',
        },
        {
          title: 'Paso 4: Solución General',
          description: 'Obtenemos la solución general incluyendo la constante de integración C',
          equation: 'y = C e^{x}',
        },
        {
          title: 'Nota',
          description: 'Error al conectar con el backend Python. Por favor verifica que el servidor Python esté corriendo en el puerto correcto.',
          equation: '\\text{Backend URL: } ' + backendUrl,
        },
      ],
    }
  }
}
