
import React, { useEffect } from 'react';

interface AppSplashScreenProps {
  appImage: string;
  onComplete: () => void;
}

const AppSplashScreen: React.FC<AppSplashScreenProps> = ({ appImage,  onComplete }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 2000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{
        backgroundImage: `url(/images/${appImage}.png)`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
      </div>
    </div>
  );
};

export default AppSplashScreen;
