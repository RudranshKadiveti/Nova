import { NextResponse } from 'next/server';
import { openDb } from '@/lib/db';

export async function GET() {
  try {
    const db = await openDb();
    const senders = await db.all('SELECT * FROM senders ORDER BY created_at DESC');
    return NextResponse.json(senders);
  } catch (error) {
    console.error('Error fetching senders:', error);
    return NextResponse.json({ error: 'Failed to fetch senders' }, { status: 500 });
  }
}
