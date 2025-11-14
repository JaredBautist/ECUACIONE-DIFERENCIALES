'use client'

import { Card } from '@/components/ui/card'
import { MathDisplay } from '@/components/math-display'
import { CheckCircle2 } from 'lucide-react'

interface Step {
  title: string
  description: string
  equation: string
}

interface SolutionStepsProps {
  steps: Step[]
}

export function SolutionSteps({ steps }: SolutionStepsProps) {
  return (
    <div className="space-y-4">
      {steps.map((step, index) => (
        <Card key={index} className="step-card p-6 hover:shadow-md transition-shadow bg-card">
          <div className="flex gap-4">
            <div className="flex-shrink-0">
              <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary font-bold">
                {index + 1}
              </div>
            </div>
            <div className="flex-1 space-y-3">
              <div className="flex items-start gap-2">
                <CheckCircle2 className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
                <div className="space-y-1">
                  <h3 className="font-semibold text-lg text-balance">{step.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{step.description}</p>
                </div>
              </div>
              <div className="pl-7 p-4 rounded-lg bg-muted/30 border border-border">
                <MathDisplay latex={step.equation} displayMode />
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  )
}
