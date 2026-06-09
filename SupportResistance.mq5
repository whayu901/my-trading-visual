//+------------------------------------------------------------------+
//|                                          SupportResistance.mq5   |
//|                        Support & Resistance - Scalping Optimized |
//|                                    Converted from Pine Script v5 |
//+------------------------------------------------------------------+
#property copyright "Optimized for Scalping XAU & Forex"
#property link      ""
#property version   "1.00"
#property indicator_chart_window
#property indicator_buffers 4
#property indicator_plots   4

//--- Plot buffers
double SupportHoldsBuffer[];
double ResistanceHoldsBuffer[];
double BreakResBuffer[];
double BreakSupBuffer[];

//--- Input parameters
input group "Settings - Optimized for Scalping"
input int    InpLookbackPeriod = 10;        // Lookback Period (8-10 for M5 scalping)
input int    InpVolFilterLength = 2;        // Delta Volume Filter Length (2-3 for scalping)
input double InpBoxWidth = 1.0;             // Adjust Box Width (ATR multiplier)

input group "Display Options"
input bool   InpShowBoxes = true;           // Show Support/Resistance Boxes
input bool   InpShowSignals = true;         // Show Diamond Signals
input color  InpSupportColor = clrGreen;    // Support Box Color
input color  InpResistanceColor = clrRed;   // Resistance Box Color

//--- Global variables
double supportLevel = 0;
double supportLower = 0;
double resistanceLevel = 0;
double resistanceUpper = 0;

datetime activeSupportStart = 0;
datetime activeResistanceStart = 0;

bool resIsSup = false;
bool supIsRes = false;

string currentSupportBoxName = "";
string currentResistanceBoxName = "";

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
{
   //--- Indicator buffers mapping
   SetIndexBuffer(0, SupportHoldsBuffer, INDICATOR_DATA);
   SetIndexBuffer(1, ResistanceHoldsBuffer, INDICATOR_DATA);
   SetIndexBuffer(2, BreakResBuffer, INDICATOR_DATA);
   SetIndexBuffer(3, BreakSupBuffer, INDICATOR_DATA);

   //--- Set plot styles
   PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ARROW);
   PlotIndexSetInteger(0, PLOT_ARROW, 108);  // Diamond symbol ◆
   PlotIndexSetInteger(0, PLOT_LINE_COLOR, InpSupportColor);
   PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2);
   PlotIndexSetString(0, PLOT_LABEL, "Support Holds");

   PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_ARROW);
   PlotIndexSetInteger(1, PLOT_ARROW, 108);  // Diamond symbol ◆
   PlotIndexSetInteger(1, PLOT_LINE_COLOR, InpResistanceColor);
   PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 2);
   PlotIndexSetString(1, PLOT_LABEL, "Resistance Holds");

   PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_ARROW);
   PlotIndexSetInteger(2, PLOT_ARROW, 108);
   PlotIndexSetInteger(2, PLOT_LINE_COLOR, InpSupportColor);
   PlotIndexSetInteger(2, PLOT_LINE_WIDTH, 2);
   PlotIndexSetString(2, PLOT_LABEL, "Break Resistance");

   PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_ARROW);
   PlotIndexSetInteger(3, PLOT_ARROW, 108);
   PlotIndexSetInteger(3, PLOT_LINE_COLOR, InpResistanceColor);
   PlotIndexSetInteger(3, PLOT_LINE_WIDTH, 2);
   PlotIndexSetString(3, PLOT_LABEL, "Break Support");

   //--- Initialize arrays
   ArraySetAsSeries(SupportHoldsBuffer, true);
   ArraySetAsSeries(ResistanceHoldsBuffer, true);
   ArraySetAsSeries(BreakResBuffer, true);
   ArraySetAsSeries(BreakSupBuffer, true);

   ArrayInitialize(SupportHoldsBuffer, EMPTY_VALUE);
   ArrayInitialize(ResistanceHoldsBuffer, EMPTY_VALUE);
   ArrayInitialize(BreakResBuffer, EMPTY_VALUE);
   ArrayInitialize(BreakSupBuffer, EMPTY_VALUE);

   //--- Set indicator name
   IndicatorSetString(INDICATOR_SHORTNAME, "SR Fast [Scalping]");

   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Custom indicator deinitialization function                       |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   //--- Delete all objects created by indicator
   ObjectsDeleteAll(0, "SR_");
   ChartRedraw();
}

//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   //--- Set arrays as series
   ArraySetAsSeries(time, true);
   ArraySetAsSeries(open, true);
   ArraySetAsSeries(high, true);
   ArraySetAsSeries(low, true);
   ArraySetAsSeries(close, true);
   ArraySetAsSeries(tick_volume, true);

   //--- Need minimum bars
   int minBars = MathMax(InpLookbackPeriod * 2 + 1, 210);
   if(rates_total < minBars)
      return(0);

   //--- Calculate from last unprocessed bar
   int limit;
   if(prev_calculated == 0)
      limit = rates_total - minBars;
   else
      limit = rates_total - prev_calculated;

   //--- Main calculation loop
   for(int i = limit; i >= 0; i--)
   {
      //--- Calculate delta volume
      double vol = DeltaVolume(i, close, open, tick_volume);
      double volHi = HighestDelta(i, InpVolFilterLength, close, open, tick_volume);
      double volLo = LowestDelta(i, InpVolFilterLength, close, open, tick_volume);

      //--- Calculate ATR and box width
      double atr = CalculateATR(i, 200, high, low, close);
      double width = atr * InpBoxWidth;

      //--- Detect new support pivot
      if(IsPivotLow(i, InpLookbackPeriod, close, rates_total) && vol > volHi)
      {
         int pivotBar = i + InpLookbackPeriod;
         if(pivotBar < rates_total)
         {
            supportLevel = close[pivotBar];
            supportLower = supportLevel - width;
            activeSupportStart = time[pivotBar];

            // Delete old box
            if(currentSupportBoxName != "")
               ObjectDelete(0, currentSupportBoxName);
         }
      }

      //--- Detect new resistance pivot
      if(IsPivotHigh(i, InpLookbackPeriod, close, rates_total) && vol < volLo)
      {
         int pivotBar = i + InpLookbackPeriod;
         if(pivotBar < rates_total)
         {
            resistanceLevel = close[pivotBar];
            resistanceUpper = resistanceLevel + width;
            activeResistanceStart = time[pivotBar];

            // Delete old box
            if(currentResistanceBoxName != "")
               ObjectDelete(0, currentResistanceBoxName);
         }
      }

      //--- Break/Hold logic
      bool breakRes = false;
      bool resHolds = false;
      bool supHolds = false;
      bool breakSup = false;

      if(i > 0 && resistanceLevel > 0 && resistanceUpper > 0)
      {
         breakRes = Crossover(low[i], resistanceUpper, low[i+1], resistanceUpper);
         resHolds = Crossunder(high[i], resistanceLevel, high[i+1], resistanceLevel);
      }

      if(i > 0 && supportLevel > 0 && supportLower > 0)
      {
         supHolds = Crossover(low[i], supportLevel, low[i+1], supportLevel);
         breakSup = Crossunder(high[i], supportLower, high[i+1], supportLower);
      }

      //--- Update flip states
      if(breakRes) resIsSup = true;
      if(resHolds) resIsSup = false;
      if(breakSup) supIsRes = true;
      if(supHolds) supIsRes = false;

      //--- Set signal buffers
      SupportHoldsBuffer[i] = EMPTY_VALUE;
      ResistanceHoldsBuffer[i] = EMPTY_VALUE;
      BreakResBuffer[i] = EMPTY_VALUE;
      BreakSupBuffer[i] = EMPTY_VALUE;

      if(InpShowSignals)
      {
         if(supHolds)
            SupportHoldsBuffer[i] = low[i] - (5 * _Point);

         if(resHolds)
            ResistanceHoldsBuffer[i] = high[i] + (5 * _Point);

         if(breakRes && resIsSup)
         {
            BreakResBuffer[i] = low[i] - (5 * _Point);
            CreateLabel("SR_BreakRes_" + IntegerToString(i), time[i], resistanceLevel,
                       "Break Res", InpSupportColor);
         }

         if(breakSup && supIsRes)
         {
            BreakSupBuffer[i] = high[i] + (5 * _Point);
            CreateLabel("SR_BreakSup_" + IntegerToString(i), time[i], supportLevel,
                       "Break Sup", InpResistanceColor);
         }
      }
   }

   //--- Draw active boxes on current bar
   if(InpShowBoxes)
   {
      //--- Support box
      if(supportLevel > 0 && supportLower > 0 && activeSupportStart > 0)
      {
         color boxColor = supIsRes ? InpResistanceColor : InpSupportColor;
         color bgColor = supIsRes ?
            ColorWithAlpha(InpResistanceColor, 220) :
            ColorWithAlpha(InpSupportColor, 230);

         currentSupportBoxName = "SR_Support_" + TimeToString(activeSupportStart);
         DrawBox(currentSupportBoxName, activeSupportStart, supportLevel,
                 time[0], supportLower, boxColor, bgColor);
      }

      //--- Resistance box
      if(resistanceLevel > 0 && resistanceUpper > 0 && activeResistanceStart > 0)
      {
         color boxColor = resIsSup ? InpSupportColor : InpResistanceColor;
         color bgColor = resIsSup ?
            ColorWithAlpha(InpSupportColor, 220) :
            ColorWithAlpha(InpResistanceColor, 230);

         currentResistanceBoxName = "SR_Resistance_" + TimeToString(activeResistanceStart);
         DrawBox(currentResistanceBoxName, activeResistanceStart, resistanceUpper,
                 time[0], resistanceLevel, boxColor, bgColor);
      }
   }

   return(rates_total);
}

//+------------------------------------------------------------------+
//| Delta Volume Calculation                                         |
//+------------------------------------------------------------------+
double DeltaVolume(int shift, const double &close[], const double &open[],
                   const long &tick_volume[])
{
   double c = close[shift];
   double o = open[shift];
   double v = (double)tick_volume[shift];

   if(c > o) return v;
   if(c < o) return -v;
   return 0;
}

//+------------------------------------------------------------------+
//| Highest Delta Volume                                             |
//+------------------------------------------------------------------+
double HighestDelta(int shift, int period, const double &close[],
                    const double &open[], const long &tick_volume[])
{
   double maxVal = -DBL_MAX;
   for(int i = 0; i < period; i++)
   {
      double v = DeltaVolume(shift + i, close, open, tick_volume) / 2.5;
      if(v > maxVal) maxVal = v;
   }
   return maxVal;
}

//+------------------------------------------------------------------+
//| Lowest Delta Volume                                              |
//+------------------------------------------------------------------+
double LowestDelta(int shift, int period, const double &close[],
                   const double &open[], const long &tick_volume[])
{
   double minVal = DBL_MAX;
   for(int i = 0; i < period; i++)
   {
      double v = DeltaVolume(shift + i, close, open, tick_volume) / 2.5;
      if(v < minVal) minVal = v;
   }
   return minVal;
}

//+------------------------------------------------------------------+
//| ATR Calculation                                                  |
//+------------------------------------------------------------------+
double CalculateATR(int shift, int period, const double &high[],
                    const double &low[], const double &close[])
{
   double sum = 0;
   for(int i = 0; i < period; i++)
   {
      int idx = shift + i;
      double h = high[idx];
      double l = low[idx];
      double pc = (idx + 1 < ArraySize(close)) ? close[idx + 1] : close[idx];

      double tr = MathMax(h - l, MathMax(MathAbs(h - pc), MathAbs(l - pc)));
      sum += tr;
   }
   return sum / period;
}

//+------------------------------------------------------------------+
//| Pivot High Detection (using close)                               |
//+------------------------------------------------------------------+
bool IsPivotHigh(int shift, int lb, const double &close[], int rates_total)
{
   int centerBar = shift + lb;
   if(centerBar + lb >= rates_total) return false;

   double center = close[centerBar];

   // Check left side
   for(int i = 0; i < lb; i++)
   {
      if(shift + i >= rates_total) return false;
      if(close[shift + i] >= center) return false;
   }

   // Check right side
   for(int i = lb + 1; i <= lb * 2; i++)
   {
      if(shift + i >= rates_total) return false;
      if(close[shift + i] >= center) return false;
   }

   return true;
}

//+------------------------------------------------------------------+
//| Pivot Low Detection (using close)                                |
//+------------------------------------------------------------------+
bool IsPivotLow(int shift, int lb, const double &close[], int rates_total)
{
   int centerBar = shift + lb;
   if(centerBar + lb >= rates_total) return false;

   double center = close[centerBar];

   // Check left side
   for(int i = 0; i < lb; i++)
   {
      if(shift + i >= rates_total) return false;
      if(close[shift + i] <= center) return false;
   }

   // Check right side
   for(int i = lb + 1; i <= lb * 2; i++)
   {
      if(shift + i >= rates_total) return false;
      if(close[shift + i] <= center) return false;
   }

   return true;
}

//+------------------------------------------------------------------+
//| Crossover Detection                                              |
//+------------------------------------------------------------------+
bool Crossover(double aNow, double bNow, double aPrev, double bPrev)
{
   return (aNow > bNow && aPrev <= bPrev);
}

//+------------------------------------------------------------------+
//| Crossunder Detection                                             |
//+------------------------------------------------------------------+
bool Crossunder(double aNow, double bNow, double aPrev, double bPrev)
{
   return (aNow < bNow && aPrev >= bPrev);
}

//+------------------------------------------------------------------+
//| Draw Rectangle Box                                               |
//+------------------------------------------------------------------+
void DrawBox(string name, datetime time1, double price1, datetime time2,
             double price2, color borderColor, color fillColor)
{
   if(ObjectFind(0, name) < 0)
   {
      ObjectCreate(0, name, OBJ_RECTANGLE, 0, time1, price1, time2, price2);
      ObjectSetInteger(0, name, OBJPROP_COLOR, borderColor);
      ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_SOLID);
      ObjectSetInteger(0, name, OBJPROP_WIDTH, 1);
      ObjectSetInteger(0, name, OBJPROP_BACK, true);
      ObjectSetInteger(0, name, OBJPROP_FILL, true);
      ObjectSetInteger(0, name, OBJPROP_BGCOLOR, fillColor);
      ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   }
   else
   {
      ObjectSetInteger(0, name, OBJPROP_TIME, 0, time1);
      ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price1);
      ObjectSetInteger(0, name, OBJPROP_TIME, 1, time2);
      ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price2);
      ObjectSetInteger(0, name, OBJPROP_COLOR, borderColor);
      ObjectSetInteger(0, name, OBJPROP_BGCOLOR, fillColor);
   }
}

//+------------------------------------------------------------------+
//| Create Text Label                                                |
//+------------------------------------------------------------------+
void CreateLabel(string name, datetime time, double price, string text, color clr)
{
   if(ObjectFind(0, name) < 0)
   {
      ObjectCreate(0, name, OBJ_TEXT, 0, time, price);
      ObjectSetString(0, name, OBJPROP_TEXT, text);
      ObjectSetInteger(0, name, OBJPROP_COLOR, clr);
      ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 8);
      ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(0, name, OBJPROP_HIDDEN, true);
   }
}

//+------------------------------------------------------------------+
//| Color with Alpha Transparency                                    |
//+------------------------------------------------------------------+
color ColorWithAlpha(color baseColor, int alpha)
{
   // alpha: 0-255 (0 = transparent, 255 = opaque)
   return (color)((alpha << 24) | (baseColor & 0xFFFFFF));
}
//+------------------------------------------------------------------+