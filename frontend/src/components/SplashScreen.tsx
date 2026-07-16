
import React, { useState, useEffect } from 'react';

interface SplashScreenProps {
  onComplete: () => void;
}

const SplashScreen: React.FC<SplashScreenProps> = ({ onComplete }) => {
  const [currentImage, setCurrentImage] = useState('/images/splash0.png');
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    // Show team.png for 3 seconds
    const timer1 = setTimeout(() => {
      setCurrentImage('/images/splash1.jpg');
    }, 3000);

    // Show firetv1.png for 3 seconds, then complete
    const timer2 = setTimeout(() => {
      setIsVisible(false);
      setTimeout(() => {
        onComplete();
      }, 500); // Allow fade out animation to complete
    }, 6000);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, [onComplete]);

  if (!isVisible) {
    return (
      <div className="fixed inset-0 bg-black flex items-center justify-center z-50 transition-opacity duration-500 opacity-0">
        <img
          src={currentImage}
          alt="Splash"
          className="max-w-full max-h-full object-contain"
        />
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black flex items-center justify-center z-50 transition-opacity duration-500">
      <img
        src={currentImage}
        alt="Splash"
        className="max-w-full max-h-full object-contain animate-fade-in"
      />
    </div>
  );
};

export default SplashScreen;
