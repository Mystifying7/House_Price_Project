import { useState, useEffect } from 'react';

export default function App() {
  const [locations, setLocations] = useState([]);
  const [formData, setFormData] = useState({ total_sqft: 1200, bhk: 2, bath: 2, location: '' });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch unique locations from Flask backend on mount
  useEffect(() => {
    fetch('https://bangalore-house-price-api.onrender.com/api/metadata')
      .then(res => res.json())
      .then(data => {
        setLocations(data.locations);
        if (data.locations.length > 0) {
          setFormData(prev => ({ ...prev, location: data.locations[0] }));
        }
      })
      .catch(err => console.error("Error fetching locations:", err));
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    
    // Prevent sub-standard area queries before firing API payload
    if (formData.total_sqft < 300) {
      alert("Area cannot be less than 300 Sq. Ft. for accurate ML prediction.");
      return;
    }

    setLoading(true);
    
    const finalPayload = {
      ...formData,
      total_sqft: formData.total_sqft || 300,
      bhk: formData.bhk || 1,
      bath: formData.bath || 1
    };

    try {
      const response = await fetch('https://bangalore-house-price-api.onrender.com/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(finalPayload)
      });
      const data = await response.json();
      setPrediction(data.predicted_price);
    } catch (err) {
      console.error("Prediction failed:", err);
    } finally {
      setLoading(false);
    }
  };

  // Helper function to format the final price beautifully
  const formatPrice = (price) => {
    if (price >= 100) {
      const crores = (price / 100).toFixed(2);
      return `₹${crores} Crores`;
    }
    return `₹${price.toFixed(2)} Lakhs`;
  };

  // Safe handler to allow manual input clearing (zero shift logic)
  const handleInputChange = (field, value) => {
    if (value === "") {
      setFormData(prev => ({ ...prev, [field]: "" }));
    } else {
      setFormData(prev => ({ ...prev, [field]: parseInt(value) || 0 }));
    }
  };

  // Enforces valid dataset baseline limits when user finishes typing
  const handleBlurValidation = (field, minValue) => {
    if (formData[field] === "" || formData[field] < minValue) {
      setFormData(prev => ({ ...prev, [field]: minValue }));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-zinc-950 text-slate-100 flex flex-col items-center justify-center p-4 relative overflow-hidden font-sans">
      
      {/* Background Decorative Premium Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-blue-500/10 rounded-full blur-[120px] pointer-events-none"></div>

      <div className="max-w-2xl w-full backdrop-blur-md bg-slate-900/70 rounded-3xl shadow-2xl p-8 md:p-10 border border-slate-800/80 relative z-10">
        
        {/* Header Section */}
        <div className="mb-8 border-b border-slate-800/60 pb-6">
          <div className="flex items-center space-x-3 mb-2">
            <span className="text-3xl">🏠</span>
            <h1 className="text-3xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-400 to-blue-500">
              PROP_ENGINE.ai
            </h1>
          </div>
          <p className="text-slate-400 text-sm leading-relaxed">
            Enterprise real estate valuation model trained on historical Bengaluru housing data vectors.
          </p>
        </div>

        {/* Input Form Layout */}
        <form onSubmit={handlePredict} className="space-y-6">
          
          {/* Location Picker */}
          <div>
            <label className="block text-xs font-semibold tracking-wider uppercase mb-2 text-slate-400">
              Target Neighborhood Location
            </label>
            <div className="relative">
              <select 
                value={formData.location}
                onChange={(e) => setFormData({...formData, location: e.target.value})}
                className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-3.5 px-4 text-slate-200 focus:outline-none focus:border-emerald-500/80 focus:ring-1 focus:ring-emerald-500/30 transition-all appearance-none cursor-pointer text-sm"
              >
                {locations.map(loc => <option key={loc} value={loc} className="bg-slate-950 text-slate-300">{loc}</option>)}
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
                ▼
              </div>
            </div>
          </div>

          {/* Grid for Parameters */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            
            {/* BHK Input */}
            <div className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-4 flex flex-col justify-between">
              <label className="block text-xs font-semibold tracking-wider uppercase text-slate-400 mb-2">
                Layout (BHK)
              </label>
              <input 
                type="number" 
                min="1"
                value={formData.bhk}
                onChange={(e) => handleInputChange('bhk', e.target.value)}
                onBlur={() => handleBlurValidation('bhk', 1)}
                className="w-full bg-transparent text-2xl font-bold text-slate-100 focus:outline-none border-b border-transparent focus:border-emerald-500/40 pb-1" 
              />
            </div>

            {/* Bathrooms Input */}
            <div className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-4 flex flex-col justify-between">
              <label className="block text-xs font-semibold tracking-wider uppercase text-slate-400 mb-2">
                Bathrooms
              </label>
              <input 
                type="number" 
                min="1"
                value={formData.bath}
                onChange={(e) => handleInputChange('bath', e.target.value)}
                onBlur={() => handleBlurValidation('bath', 1)}
                className="w-full bg-transparent text-2xl font-bold text-slate-100 focus:outline-none border-b border-transparent focus:border-emerald-500/40 pb-1" 
              />
            </div>

            {/* Area Sqft Input */}
            <div className="bg-slate-950/40 border border-slate-800/60 rounded-2xl p-4 flex flex-col justify-between">
              <label className="block text-xs font-semibold tracking-wider uppercase text-slate-400 mb-2">
                Area (Sq. Ft.)
              </label>
              <input 
                type="number" 
                min="300"
                value={formData.total_sqft}
                onChange={(e) => handleInputChange('total_sqft', e.target.value)}
                onBlur={() => handleBlurValidation('total_sqft', 300)}
                className="w-full bg-transparent text-2xl font-bold text-slate-100 focus:outline-none border-b border-transparent focus:border-emerald-500/40 pb-1" 
              />
            </div>

          </div>

          {/* Action Trigger Button */}
          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-4 bg-gradient-to-r from-emerald-500 via-teal-500 to-blue-600 hover:opacity-95 text-slate-950 font-black rounded-xl tracking-wider uppercase text-xs shadow-lg shadow-emerald-500/10 transition-all duration-300 transform active:scale-[0.99] disabled:opacity-40"
          >
            {loading ? (
              <span className="flex items-center justify-center space-x-2">
                <svg className="animate-spin h-4 w-4 text-slate-950" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                <span>Processing Vectors...</span>
              </span>
            ) : '🔮 Run ML Valuation Engine'}
          </button>
        </form>

        {/* Dynamic Output Presentation */}
        {prediction !== null && (
          <div className="mt-8 pt-6 border-t border-slate-800/80 text-center animate-[fadeIn_0.4s_ease-out]">
            <h3 className="text-slate-500 text-xs font-bold uppercase tracking-widest">
              Estimated Market Valuation
            </h3>
            <div className="inline-block mt-3 p-6 px-10 bg-gradient-to-b from-slate-950 to-slate-950/40 border border-emerald-500/20 rounded-2xl shadow-inner">
              <p className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300 tracking-tight">
                {formatPrice(prediction)}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Subtle Mini Footer */}
      <div className="mt-6 text-[10px] tracking-widest uppercase text-slate-600 relative z-10">
        System Status: Operational • API Port: 5000
      </div>
    </div>
  );
}