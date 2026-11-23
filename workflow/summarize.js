// Run after loopStuck. If the loop result shape differs in your editor,
// inspect one run and adjust the mapper so `escalated` is a real count.
const rows = loopStuck.data || [];
const escalated = rows
  .map((r) => (Array.isArray(r) ? r[0] : r?.escalateOne?.data?.[0] || r?.data?.[0] || r))
  .filter(Boolean);

return {
  ok: true,
  escalated: escalated.length,
  tickets: escalated.map((r) => r.ticket_number || r.id),
};
