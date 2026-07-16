
import React from 'react';

interface Game {
  id: string;
  name: string;
  icon: string;
  color: string;
  category: string;
  imageName: string;
}

const games: Game[] = [
  { id: 'clash-royale', name: 'Clash Royale', icon: '⚔️', color: 'bg-purple-600', category: 'Strategy', imageName: 'game6' },
  { id: 'fortnite', name: 'Fortnite', icon: '🎮', color: 'bg-indigo-600', category: 'Battle Royale', imageName: 'game7' },
  { id: 'minecraft', name: 'Minecraft', icon: '🧱', color: 'bg-green-500', category: 'Sandbox', imageName: 'game8' },
  { id: 'crossy-road', name: 'Crossy Road', icon: '🐸', color: 'bg-green-600', category: 'Arcade', imageName: 'image01' },
  { id: 'temple-run', name: 'Temple Run', icon: '🏃', color: 'bg-orange-600', category: 'Adventure', imageName: 'game2' },
  { id: 'candy-crush', name: 'Candy Crush', icon: '🍭', color: 'bg-pink-600', category: 'Puzzle', imageName: 'game3' },
  { id: 'angry-birds', name: 'Angry Birds', icon: '🐦', color: 'bg-red-600', category: 'Arcade', imageName: 'game4' },
  { id: 'subway-surfers', name: 'Subway Surfers', icon: '🚇', color: 'bg-blue-600', category: 'Action', imageName: 'game5' }
  
];

const GamesPage = () => {
  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Games</h1>
        
        <div className="grid grid-cols-4 gap-8">
          {games.map((game) => (
            <div
              key={game.id}
              className="cursor-pointer group"
            >
              <div
                className="w-full h-40 rounded-xl overflow-hidden relative transition-all duration-300 group-hover:scale-105 group-hover:shadow-2xl"
                style={{
                  backgroundImage: `url(/images/${game.imageName}.png)`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                  backgroundColor: game.color
                }}
              >
                <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                <div className="absolute bottom-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
                  {game.category}
                </div>
              </div>
              <div className="text-center mt-3">
                <p className="text-white font-medium group-hover:text-fire-orange transition-colors">
                  {game.name}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GamesPage;
