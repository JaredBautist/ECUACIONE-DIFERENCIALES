'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Calculator, Sparkles, Brain, BookOpen } from 'lucide-react'
import { MathDisplay } from '@/components/math-display'
import { SolutionSteps } from '@/components/solution-steps'
import { solveDifferentialEquation } from '@/lib/de-solver'
import { ExampleExercises } from '@/components/example-exercises'

const equationTypes = [
  { value: 'separable', label: 'Variables Separables' },
  { value: 'homogeneous', label: 'Homogéneas' },
  { value: 'exact', label: 'Exactas' },
  { value: 'linear', label: 'Lineales' },
  { value: 'bernoulli', label: 'Bernoulli' },
  { value: 'reducible', label: 'Reducibles a Primer Orden' },
  { value: 'constant-coef', label: 'Coeficientes Constantes' },
  { value: 'undetermined', label: 'Coeficientes Indeterminados' },
  { value: 'integrating-factor', label: 'Factor Integrante' },
]

export default function DifferentialEquationSolver() {
  const [equation, setEquation] = useState('')
  const [equationType, setEquationType] = useState('separable')
  const [solution, setSolution] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSolve = async () => {
    if (!equation.trim()) return
    
    setIsLoading(true)
    try {
      const result = await solveDifferentialEquation(equation, equationType)
      setSolution(result)
    } catch (error) {
      console.error('[v0] Error solving equation:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleExerciseSelect = (selectedEquation: string, selectedType: string) => {
    setEquation(selectedEquation)
    setEquationType(selectedType)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary text-primary-foreground">
              <Calculator className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-balance">DiffEQ Solver</h1>
              <p className="text-sm text-muted-foreground">Resolvedor de Ecuaciones Diferenciales</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="grid gap-6 lg:grid-cols-[1fr_400px]">
          {/* Input Section */}
          <div className="space-y-6">
            <Card className="border-2 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="w-5 h-5 text-primary" />
                  Ingresa tu Ecuación Diferencial
                </CardTitle>
                <CardDescription>
                  Escribe la ecuación y selecciona el tipo para obtener la solución paso a paso
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="equation-type">Tipo de Ecuación</Label>
                  <Select value={equationType} onValueChange={setEquationType}>
                    <SelectTrigger id="equation-type">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {equationTypes.map((type) => (
                        <SelectItem key={type.value} value={type.value}>
                          {type.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="equation">Ecuación Diferencial</Label>
                  <Input
                    id="equation"
                    placeholder="ej: dy/dx = x*y"
                    value={equation}
                    onChange={(e) => setEquation(e.target.value)}
                    className="font-mono text-lg"
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !isLoading) {
                        handleSolve()
                      }
                    }}
                  />
                  <p className="text-xs text-muted-foreground">
                    Usa notación estándar: dy/dx, y', x^2, sqrt(x), etc.
                  </p>
                </div>

                <Button 
                  onClick={handleSolve} 
                  disabled={isLoading || !equation.trim()}
                  className="w-full h-12 text-lg font-semibold shadow-lg hover:shadow-xl transition-shadow"
                  size="lg"
                >
                  {isLoading ? (
                    <>
                      <span className="animate-spin mr-2">⏳</span>
                      Resolviendo...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5 mr-2" />
                      Resolver Ecuación
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* Solution Display */}
            {solution && (
              <Card className="border-2 shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-primary">
                    <BookOpen className="w-5 h-5" />
                    Solución
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="solution" className="w-full">
                    <TabsList className="grid w-full grid-cols-2">
                      <TabsTrigger value="solution">Resultado Final</TabsTrigger>
                      <TabsTrigger value="steps">Paso a Paso</TabsTrigger>
                    </TabsList>
                    <TabsContent value="solution" className="mt-6">
                      <div className="space-y-4">
                        <div className="p-6 rounded-lg bg-muted/50 border-2 border-primary/20">
                          <p className="text-sm font-semibold text-muted-foreground mb-2">
                            Ecuación Original:
                          </p>
                          <MathDisplay latex={solution.originalEquation} />
                        </div>
                        <div className="p-6 rounded-lg bg-primary/10 border-2 border-primary">
                          <p className="text-sm font-semibold text-primary mb-2">
                            Solución General:
                          </p>
                          <MathDisplay latex={solution.solution} displayMode />
                        </div>
                      </div>
                    </TabsContent>
                    <TabsContent value="steps" className="mt-6">
                      <SolutionSteps steps={solution.steps} />
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Info Sidebar */}
          <div className="space-y-6">
            <ExampleExercises onSelectExercise={handleExerciseSelect} />
            
            <Card className="border-2 shadow-lg bg-gradient-to-br from-primary/5 to-secondary/5">
              <CardHeader>
                <CardTitle className="text-lg">Tipos de Ecuaciones Soportadas</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  {equationTypes.map((type, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-primary font-bold">•</span>
                      <span>{type.label}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 shadow-lg bg-gradient-to-br from-secondary/5 to-accent/5">
              <CardHeader>
                <CardTitle className="text-lg">Ejemplos de Notación</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-sm font-semibold text-muted-foreground mb-1">Derivadas:</p>
                  <p className="text-sm font-mono bg-muted/50 p-2 rounded">dy/dx, y', y''</p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-muted-foreground mb-1">Operaciones:</p>
                  <p className="text-sm font-mono bg-muted/50 p-2 rounded">x^2, sqrt(x), e^x, ln(x)</p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-muted-foreground mb-1">Trigonométricas:</p>
                  <p className="text-sm font-mono bg-muted/50 p-2 rounded">sin(x), cos(x), tan(x)</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
