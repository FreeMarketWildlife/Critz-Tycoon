// Review playback only: source-derived gait timing, independent of game state.
export const TICK_MS = 1000 * 280896 / 16777216;
export const DIRECTIONS = ['south', 'west', 'north', 'east'];
export const POSES = ['strideA', 'idle', 'strideB', 'idle'];
export const HOLD_TICKS = 8;
export const DIRECTION_TICKS = 96;
export function poseAt(tick) { return POSES[Math.floor(tick / HOLD_TICKS) % POSES.length]; }
export function directionAt(tick) { return DIRECTIONS[Math.floor(tick / DIRECTION_TICKS) % DIRECTIONS.length]; }
export function createReviewClock() {
  let tick = 0, accumulator = 0, previous = null, droppedMs = 0;
  return {
    advance(now) {
      if (previous === null) { previous = now; return 0; }
      const elapsed = Math.max(0, now - previous); previous = now;
      // A suspended/long frame never causes accelerated catch-up in the review.
      if (elapsed > 250) { droppedMs += elapsed; accumulator = 0; return 0; }
      accumulator += elapsed;
      const count = Math.floor((accumulator + 1e-7) / TICK_MS);
      tick += count; accumulator -= count * TICK_MS;
      return count;
    },
    resetBaseline() { previous = null; accumulator = 0; },
    nextPose() { tick = (Math.floor(tick / HOLD_TICKS) + 1) * HOLD_TICKS; previous = null; accumulator = 0; },
    restart() { tick = 0; previous = null; accumulator = 0; },
    get tick() { return tick; },
    get droppedMs() { return droppedMs; },
  };
}
