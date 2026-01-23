import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    success: true,
    message: 'Financial Health Survey API is running',
    status: 'healthy',
    model_trained: true,
    timestamp: new Date().toISOString()
  });
}