import { NextResponse } from 'next/server';
import { openDb } from '@/lib/db';

export async function PUT(request, { params }) {
  try {
    const { id } = await params;
    const body = await request.json();
    const { action_rule } = body;

    if (!['ask', 'auto-sync', 'ignore'].includes(action_rule)) {
      return NextResponse.json({ error: 'Invalid action_rule' }, { status: 400 });
    }

    const db = await openDb();
    await db.run('UPDATE senders SET action_rule = ? WHERE id = ?', [action_rule, id]);
    
    return NextResponse.json({ success: true, message: `Sender ${id} updated to ${action_rule}` });
  } catch (error) {
    console.error('Error updating sender:', error);
    return NextResponse.json({ error: 'Failed to update sender' }, { status: 500 });
  }
}
