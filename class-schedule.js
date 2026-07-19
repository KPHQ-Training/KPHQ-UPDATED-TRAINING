// KeyPlayers VA Academy — Class Schedule (single source of truth for the cohort start date)
//
// TO LAUNCH A NEW CLASS: change CLASS_START_DATE below to the new cohort's Day 1.
// It must be a Monday — the course runs Mon-Fri, 2 work-weeks, skipping the
// weekend in between (Day 1 Mon ... Day 5 Fri, Day 6 Mon ... Day 10 Fri).
// That's the only edit needed — every Day page computes its own unlock date
// from this automatically via DAY_INDEX in its CONFIG.
window.CLASS_START_DATE = '2026-07-20';

// Returns the unlock Date (midnight Eastern) for a given day index
// (1 = Day 1 ... 10 = Day 10), counting weekdays only.
window.kpUnlockDateForDay = function (dayIndex) {
  var d = new Date(window.CLASS_START_DATE + 'T00:00:00-04:00');
  var added = 0;
  while (added < dayIndex - 1) {
    d.setDate(d.getDate() + 1);
    var dow = d.getDay();
    if (dow !== 0 && dow !== 6) added++;
  }
  return d;
};
