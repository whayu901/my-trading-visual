//@version=1

init = () => {
  indicator({ onMainPanel: true, format: "inherit" });

  input.int("Lookback Period", 10, "lookback", 1, 100, 1, "Optimized for scalping", "Settings");
  input.int("Delta Volume Filter Length", 2, "vollen", 1, 50, 1, "Higher = fewer boxes", "Settings");
  input.float("Adjust Box Width", 1.0, "boxwidth", 0.1, 1000, 0.1, "ATR multiplier", "Settings");

  input.bool("Show Boxes", true, "showboxes", "Show support/resistance boxes", "Display");
  input.bool("Show Signals", true, "showsignals", "Show diamond signals", "Display");
};

// =============================
// STATE
// =============================
let supportLevel = null;
let supportLower = null;
let resistanceLevel = null;
let resistanceUpper = null;

let activeSupportStart = null;
let activeResistanceStart = null;

let resIsSup = false;
let supIsRes = false;

// =============================
// HELPERS - USING ARRAY NOTATION
// =============================
const getClose = (offset) => {
  try {
    // Try different methods
    if (typeof close === 'function') {
      return close();
    } else if (Array.isArray(close)) {
      return close[offset];
    } else if (close && typeof close === 'object' && close[offset] !== undefined) {
      return close[offset];
    }
    return 0;
  } catch (e) {
    return 0;
  }
};

const getOpen = (offset) => {
  try {
    if (typeof open === 'function') {
      return open();
    } else if (Array.isArray(open)) {
      return open[offset];
    } else if (open && typeof open === 'object' && open[offset] !== undefined) {
      return open[offset];
    }
    return 0;
  } catch (e) {
    return 0;
  }
};

const getHigh = (offset) => {
  try {
    if (typeof high === 'function') {
      return high();
    } else if (Array.isArray(high)) {
      return high[offset];
    } else if (high && typeof high === 'object' && high[offset] !== undefined) {
      return high[offset];
    }
    return 0;
  } catch (e) {
    return 0;
  }
};

const getLow = (offset) => {
  try {
    if (typeof low === 'function') {
      return low();
    } else if (Array.isArray(low)) {
      return low[offset];
    } else if (low && typeof low === 'object' && low[offset] !== undefined) {
      return low[offset];
    }
    return 0;
  } catch (e) {
    return 0;
  }
};

const getVolume = (offset) => {
  try {
    if (typeof volume === 'function') {
      return volume();
    } else if (Array.isArray(volume)) {
      return volume[offset];
    } else if (volume && typeof volume === 'object' && volume[offset] !== undefined) {
      return volume[offset];
    }
    return 0;
  } catch (e) {
    return 0;
  }
};

const getTime = (offset) => {
  try {
    if (typeof time === 'function') {
      return time();
    } else if (Array.isArray(time)) {
      return time[offset];
    } else if (time && typeof time === 'object' && time[offset] !== undefined) {
      return time[offset];
    }
    return Date.now();
  } catch (e) {
    return Date.now();
  }
};

const deltaVolume = (offset) => {
  const c = getClose(offset);
  const o = getOpen(offset);
  const v = getVolume(offset);

  if (c > o) return v;
  if (c < o) return -v;
  return 0;
};

const highestDelta = (len) => {
  let maxVal = -Infinity;
  for (let i = 0; i < len; i++) {
    const v = deltaVolume(i) / 2.5;
    if (v > maxVal) maxVal = v;
  }
  return maxVal;
};

const lowestDelta = (len) => {
  let minVal = Infinity;
  for (let i = 0; i < len; i++) {
    const v = deltaVolume(i) / 2.5;
    if (v < minVal) minVal = v;
  }
  return minVal;
};

const trueRange = (offset) => {
  const h = getHigh(offset);
  const l = getLow(offset);
  const pc = getClose(offset + 1);

  return Math.max(
    h - l,
    Math.abs(h - pc),
    Math.abs(l - pc)
  );
};

const atr = (period) => {
  let sum = 0;
  for (let i = 0; i < period; i++) {
    sum += trueRange(i);
  }
  return sum / period;
};

const isPivotHighClose = (lb) => {
  const center = getClose(lb);

  // Check left side
  for (let i = 0; i < lb; i++) {
    if (getClose(i) >= center) {
      return false;
    }
  }

  // Check right side
  for (let i = lb + 1; i <= lb * 2; i++) {
    if (getClose(i) >= center) {
      return false;
    }
  }

  return true;
};

const isPivotLowClose = (lb) => {
  const center = getClose(lb);

  // Check left side
  for (let i = 0; i < lb; i++) {
    if (getClose(i) <= center) {
      return false;
    }
  }

  // Check right side
  for (let i = lb + 1; i <= lb * 2; i++) {
    if (getClose(i) <= center) {
      return false;
    }
  }

  return true;
};

const crossover = (aNow, bNow, aPrev, bPrev) => {
  return aNow > bNow && aPrev <= bPrev;
};

const crossunder = (aNow, bNow, aPrev, bPrev) => {
  return aNow < bNow && aPrev >= bPrev;
};

// =============================
// MAIN
// =============================
onTick = (length, _moment, _, ta, inputs) => {
  const lb = inputs.lookback;
  const volLen = inputs.vollen;
  const boxWidth = inputs.boxwidth;
  const showBoxes = inputs.showboxes;
  const showSignals = inputs.showsignals;

  const minBars = Math.max(lb * 2 + 1, 210);
  if (length < minBars) {
    return;
  }

  // DEBUG: Check data access
  if (length === minBars) {
    console.log("=== DEBUG START ===");
    console.log("Length:", length);
    console.log("Close test:", getClose(0), getClose(1), getClose(2));
    console.log("High test:", getHigh(0), getHigh(1));
    console.log("Low test:", getLow(0), getLow(1));
    console.log("Volume test:", getVolume(0), getVolume(1));
    console.log("Time test:", getTime(0), getTime(1));
    console.log("ta object:", ta);
    console.log("=== DEBUG END ===");
  }

  const vol = deltaVolume(0);
  const volHi = highestDelta(volLen);
  const volLo = lowestDelta(volLen);
  const width = atr(200) * boxWidth;

  // =============================
  // NEW SUPPORT PIVOT
  // =============================
  if (isPivotLowClose(lb) && vol > volHi) {
    const pivotTime = getTime(lb);
    const newSupportLevel = getClose(lb);
    const newSupportLower = newSupportLevel - width;

    supportLevel = newSupportLevel;
    supportLower = newSupportLower;
    activeSupportStart = pivotTime;

    console.log("✅ SUPPORT PIVOT FOUND at", newSupportLevel, "time:", pivotTime);
  }

  // =============================
  // NEW RESISTANCE PIVOT
  // =============================
  if (isPivotHighClose(lb) && vol < volLo) {
    const pivotTime = getTime(lb);
    const newResistanceLevel = getClose(lb);
    const newResistanceUpper = newResistanceLevel + width;

    resistanceLevel = newResistanceLevel;
    resistanceUpper = newResistanceUpper;
    activeResistanceStart = pivotTime;

    console.log("✅ RESISTANCE PIVOT FOUND at", newResistanceLevel, "time:", pivotTime);
  }

  // =============================
  // BREAK / HOLD LOGIC
  // =============================
  let breakRes = false;
  let resHolds = false;
  let supHolds = false;
  let breakSup = false;

  if (resistanceLevel !== null && resistanceUpper !== null) {
    breakRes = crossover(getLow(0), resistanceUpper, getLow(1), resistanceUpper);
    resHolds = crossunder(getHigh(0), resistanceLevel, getHigh(1), resistanceLevel);
  }

  if (supportLevel !== null && supportLower !== null) {
    supHolds = crossover(getLow(0), supportLevel, getLow(1), supportLevel);
    breakSup = crossunder(getHigh(0), supportLower, getHigh(1), supportLower);
  }

  if (breakRes) resIsSup = true;
  if (resHolds) resIsSup = false;

  if (breakSup) supIsRes = true;
  if (supHolds) supIsRes = false;

  // =============================
  // DRAW BOXES
  // =============================
  if (showBoxes) {
    // Support box
    if (activeSupportStart !== null && supportLevel !== null && supportLower !== null) {
      const supBroken = supIsRes;
      const supColor = supBroken ? color.red : color.green;
      const supBgColor = supBroken ? color.rgba(255, 0, 0, 0.8) : color.rgba(0, 128, 0, 0.7);

      if (length % 50 === 0) {
        console.log("📦 Drawing SUPPORT box:", {
          start: activeSupportStart,
          top: supportLevel,
          bottom: supportLower,
          broken: supBroken
        });
      }

      rectangle(
        activeSupportStart,
        supportLevel,
        getTime(0),
        supportLower,
        {
          backgroundColor: supBgColor,
          color: supColor,
          linewidth: 1,
          extendRight: true
        }
      );
    }

    // Resistance box
    if (activeResistanceStart !== null && resistanceLevel !== null && resistanceUpper !== null) {
      const resBroken = resIsSup;
      const resColor = resBroken ? color.green : color.red;
      const resBgColor = resBroken ? color.rgba(0, 128, 0, 0.8) : color.rgba(255, 0, 0, 0.7);

      rectangle(
        activeResistanceStart,
        resistanceUpper,
        getTime(0),
        resistanceLevel,
        {
          backgroundColor: resBgColor,
          color: resColor,
          linewidth: 1,
          extendRight: true
        }
      );
    }
  }

  // =============================
  // SIGNALS - COMMENTED OUT TEMPORARILY
  // TODO: Need correct plot.shapes() signature from FX Replay docs
  // =============================
  if (showSignals) {
    const currentTime = getTime(0);
    const currentLow = getLow(0);
    const currentHigh = getHigh(0);

    // TEMPORARY: Using simple plot lines instead of shapes
    if (supHolds) {
      plot.line("Support Holds", currentLow, color.lime, 3);
    }

    if (resHolds) {
      plot.line("Resistance Holds", currentHigh, color.red, 3);
    }

    if (breakRes && resIsSup) {
      plot.line("Res as Sup", currentLow, color.lime, 3);
    }

    if (breakSup && supIsRes) {
      plot.line("Sup as Res", currentHigh, color.red, 3);
    }
  }

  // UNCOMMENT WHEN WE KNOW CORRECT SIGNATURE:
  /*
  if (showSignals) {
    const currentTime = getTime(0);
    const currentLow = getLow(0);
    const currentHigh = getHigh(0);

    if (supHolds) {
      plot.shapes(
        "Support Holds",      // id
        currentTime,          // time
        currentLow * 0.9995,  // price
        "diamond",            // shape
        color.lime,           // color
        4,                    // size
        color.white,          // textColor?
        "",                   // text?
        // ??? more params needed
      );
    }
  }
  */
};