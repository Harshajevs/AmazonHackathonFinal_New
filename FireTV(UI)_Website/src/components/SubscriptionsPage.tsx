
import React from 'react';
import { Check, X, Star } from 'lucide-react';

interface Subscription {
  id: string;
  name: string;
  price: string;
  status: 'active' | 'inactive';
  nextBilling?: string;
  features: string[];
  color: string;
  type: 'basic' | 'premium' | 'family';
}

const mySubscriptions: Subscription[] = [
  {
    id: 'prime-premium',
    name: 'Amazon Prime Video Premium',
    price: '$14.99/month',
    status: 'active',
    nextBilling: 'Dec 25, 2024',
    features: ['4K Ultra HD', 'Download for offline', 'Multiple devices', 'Prime benefits'],
    color: 'bg-blue-600',
    type: 'premium'
  },
  {
    id: 'netflix-standard',
    name: 'Netflix Standard',
    price: '$15.99/month',
    status: 'active',
    nextBilling: 'Jan 10, 2025',
    features: ['HD streaming', '2 screens', 'Download feature', 'No ads'],
    color: 'bg-red-600',
    type: 'premium'
  },
  {
    id: 'youtube-premium',
    name: 'YouTube Premium',
    price: '$11.99/month',
    status: 'active',
    nextBilling: 'Dec 30, 2024',
    features: ['Ad-free videos', 'Background play', 'YouTube Music', 'Downloads'],
    color: 'bg-red-500',
    type: 'premium'
  }
];

const availableSubscriptions: Subscription[] = [
  {
    id: 'prime-basic',
    name: 'Amazon Prime Video Basic',
    price: '$8.99/month',
    status: 'inactive',
    features: ['HD streaming', 'Limited ads', 'Download for offline'],
    color: 'bg-blue-600',
    type: 'basic'
  },
  {
    id: 'netflix-basic',
    name: 'Netflix Basic',
    price: '$6.99/month',
    status: 'inactive',
    features: ['720p streaming', '1 screen', 'Limited downloads'],
    color: 'bg-red-600',
    type: 'basic'
  },
  {
    id: 'netflix-premium',
    name: 'Netflix Premium',
    price: '$22.99/month',
    status: 'inactive',
    features: ['4K Ultra HD', '4 screens', 'Unlimited downloads', 'Spatial audio'],
    color: 'bg-red-600',
    type: 'family'
  },
  {
    id: 'hotstar-premium',
    name: 'Disney+ Hotstar Premium',
    price: '$9.99/month',
    status: 'inactive',
    features: ['Live sports', 'Disney content', 'Local content', '4K streaming'],
    color: 'bg-purple-600',
    type: 'premium'
  },
  {
    id: 'hotstar-vip',
    name: 'Disney+ Hotstar VIP',
    price: '$4.99/month',
    status: 'inactive',
    features: ['Live sports', 'Local content', 'HD streaming'],
    color: 'bg-purple-600',
    type: 'basic'
  },
  {
    id: 'spotify-premium',
    name: 'Spotify Premium',
    price: '$9.99/month',
    status: 'inactive',
    features: ['Ad-free music', 'Offline downloads', 'High quality audio', 'Unlimited skips'],
    color: 'bg-green-500',
    type: 'premium'
  },
  {
    id: 'spotify-family',
    name: 'Spotify Family',
    price: '$15.99/month',
    status: 'inactive',
    features: ['6 accounts', 'Ad-free music', 'Offline downloads', 'Kids profiles'],
    color: 'bg-green-500',
    type: 'family'
  },
  {
    id: 'aha-premium',
    name: 'Aha Premium',
    price: '$6.99/month',
    status: 'inactive',
    features: ['Regional content', 'Original series', 'HD streaming', 'No ads'],
    color: 'bg-orange-600',
    type: 'premium'
  },
  {
    id: 'aha-basic',
    name: 'Aha Basic',
    price: '$2.99/month',
    status: 'inactive',
    features: ['Regional content', 'Limited ads', 'SD streaming'],
    color: 'bg-orange-600',
    type: 'basic'
  }
];

const SubscriptionsPage = () => {
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'premium':
        return <Star size={16} className="text-yellow-400" />;
      case 'family':
        return <span className="text-xs font-bold text-blue-400">FAM</span>;
      default:
        return null;
    }
  };

  const renderSubscriptionCard = (sub: Subscription, isActive: boolean = false) => (
    <div
      key={sub.id}
      className="bg-fire-dark rounded-xl p-6 border border-fire-gray/30 hover:border-fire-orange/50 transition-all duration-200"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-4">
          <div className={`w-12 h-12 ${sub.color} rounded-lg flex items-center justify-center`}>
            <span className="text-white font-bold text-lg">
              {sub.name.charAt(0)}
            </span>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-xl font-semibold text-white">{sub.name}</h3>
              {getTypeIcon(sub.type)}
            </div>
            <p className="text-fire-orange font-medium">{sub.price}</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {isActive ? (
            <div className="flex items-center space-x-1 text-green-400">
              <Check size={16} />
              <span className="text-sm">Active</span>
            </div>
          ) : (
            <div className="flex items-center space-x-1 text-gray-400">
              <X size={16} />
              <span className="text-sm">Available</span>
            </div>
          )}
        </div>
      </div>
      
      {sub.nextBilling && (
        <p className="text-gray-400 text-sm mb-4">
          Next billing: {sub.nextBilling}
        </p>
      )}
      
      <div className="space-y-2 mb-6">
        {sub.features.map((feature, index) => (
          <div key={index} className="flex items-center space-x-2">
            <Check size={14} className="text-fire-orange" />
            <span className="text-gray-300 text-sm">{feature}</span>
          </div>
        ))}
      </div>
      
      <div className="flex space-x-3">
        <button className="flex-1 bg-fire-orange hover:bg-fire-orange/80 text-white py-2 px-4 rounded-lg transition-colors">
          {isActive ? 'Manage' : 'Subscribe'}
        </button>
        {isActive && (
          <button className="px-4 py-2 border border-gray-600 text-gray-300 hover:text-white hover:border-gray-500 rounded-lg transition-colors">
            Cancel
          </button>
        )}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Subscriptions</h1>
        
        {/* My Subscriptions */}
        <div className="mb-12">
          <h2 className="text-2xl font-semibold text-white mb-6">My Subscriptions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mySubscriptions.map((sub) => renderSubscriptionCard(sub, true))}
          </div>
        </div>

        {/* Available Subscriptions */}
        <div>
          <h2 className="text-2xl font-semibold text-white mb-6">Available Subscriptions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {availableSubscriptions.map((sub) => renderSubscriptionCard(sub, false))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionsPage;
