/**
 * API Connection Status Component
 * Shows the current connection status to the backend API
 */
"use client";

import { useState, useEffect } from 'react';
import { checkApiHealth, getApiUrl } from '@/lib/api';

export default function ApiStatus() {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkHealth = async () => {
    setIsChecking(true);
    try {
      const healthy = await checkApiHealth();
      setIsHealthy(healthy);
      setLastChecked(new Date());
    } catch (error) {
      console.error('Health check error:', error);
      setIsHealthy(false);
      setLastChecked(new Date());
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    // Check on mount
    checkHealth();
    
    // Set up periodic health checks (every 30 seconds)
    const interval = setInterval(checkHealth, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    if (isChecking) return 'text-yellow-600';
    if (isHealthy === null) return 'text-gray-600';
    return isHealthy ? 'text-green-600' : 'text-red-600';
  };

  const getStatusText = () => {
    if (isChecking) return 'Checking...';
    if (isHealthy === null) return 'Unknown';
    return isHealthy ? 'Connected' : 'Disconnected';
  };

  return (
    <div className="inline-flex items-center gap-2 px-3 py-1 bg-gray-100 dark:bg-gray-800 rounded-full text-sm">
      <div className={`w-2 h-2 rounded-full ${isChecking ? 'animate-pulse bg-yellow-500' : isHealthy ? 'bg-green-500' : 'bg-red-500'}`} />
      <span className={getStatusColor()}>
        API: {getStatusText()}
      </span>
      <button
        onClick={checkHealth}
        disabled={isChecking}
        className="text-xs opacity-70 hover:opacity-100 underline"
      >
        {isChecking ? '...' : 'Refresh'}
      </button>
      {lastChecked && (
        <span className="text-xs opacity-50">
          {lastChecked.toLocaleTimeString()}
        </span>
      )}
      <div className="text-xs opacity-50 hidden sm:block">
        {getApiUrl()}
      </div>
    </div>
  );
}