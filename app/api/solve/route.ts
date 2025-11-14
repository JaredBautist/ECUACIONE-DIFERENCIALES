import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { equation, equationType } = await request.json()

    if (!equation || !equationType) {
      return NextResponse.json(
        { error: 'Equation and equation type are required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${process.env.PYTHON_BACKEND_URL || 'http://localhost:8000'}/solve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        equation,
        equation_type: equationType,
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to solve equation')
    }

    const result = await response.json()
    return NextResponse.json(result)
  } catch (error) {
    console.error('[v0] Error solving equation:', error)
    return NextResponse.json(
      { error: 'Failed to solve equation' },
      { status: 500 }
    )
  }
}
