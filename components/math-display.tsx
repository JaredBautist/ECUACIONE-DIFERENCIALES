'use client'

import { useEffect, useRef } from 'react'
import katex from 'katex'

interface MathDisplayProps {
  latex: string
  displayMode?: boolean
}

export function MathDisplay({ latex, displayMode = false }: MathDisplayProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (containerRef.current && latex) {
      try {
        katex.render(latex, containerRef.current, {
          displayMode,
          throwOnError: false,
          errorColor: '#cc0000',
          strict: false,
          trust: false,
        })
      } catch (error) {
        console.error('[v0] KaTeX rendering error:', error)
        if (containerRef.current) {
          containerRef.current.textContent = latex
        }
      }
    }
  }, [latex, displayMode])

  return (
    <div 
      ref={containerRef}
      className={`select-text ${displayMode ? 'text-center text-xl' : 'inline-block text-lg'}`}
    />
  )
}
