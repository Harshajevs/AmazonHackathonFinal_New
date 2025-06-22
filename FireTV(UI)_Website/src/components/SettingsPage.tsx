import React, { useState } from 'react';
import { ChevronRight, Wifi, Cast, Monitor, Volume2, Users, Shield, HelpCircle, Info, Bluetooth, Smartphone, Download } from 'lucide-react';

interface SettingItem {
  id: string;
  title: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  description: string;
  value?: string;
}

const settingsCategories = [
  {
    title: 'Network & Internet',
    items: [
      { id: 'wifi', title: 'Wi-Fi', icon: Wifi, description: 'Connected to Home Network', value: 'Connected' },
      { id: 'bluetooth', title: 'Bluetooth', icon: Bluetooth, description: 'Connect wireless devices', value: 'Off' },
      { id: 'ethernet', title: 'Ethernet', icon: Cast, description: 'Wired connection settings', value: 'Not connected' }
    ]
  },
  {
    title: 'Display & Sound',
    items: [
      { id: 'display', title: 'Display Settings', icon: Monitor, description: 'Resolution, HDR, and screen settings', value: '4K HDR' },
      { id: 'audio', title: 'Audio Settings', icon: Volume2, description: 'Sound mode and audio output', value: 'Dolby Digital' },
      { id: 'screensaver', title: 'Screen Saver', icon: Monitor, description: 'Screen saver and sleep settings', value: '10 minutes' },
      { id: 'screenshare', title: 'Screen Sharing', icon: Smartphone, description: 'Cast from mobile devices', value: 'Enabled' }
    ]
  },
  {
    title: 'Accounts & Privacy',
    items: [
      { id: 'accounts', title: 'Account Settings', icon: Users, description: 'Manage user accounts and profiles', value: '2 accounts' },
      { id: 'privacy', title: 'Privacy Settings', icon: Shield, description: 'Data usage and privacy controls', value: 'Customized' },
      { id: 'parental', title: 'Parental Controls', icon: Shield, description: 'Content restrictions and PIN', value: 'Off' }
    ]
  },
  {
    title: 'System',
    items: [
      { id: 'updates', title: 'System Updates', icon: Download, description: 'Check for software updates', value: 'Up to date' },
      { id: 'storage', title: 'Storage', icon: Monitor, description: 'Manage device storage', value: '45% used' },
      { id: 'about', title: 'About', icon: Info, description: 'System information and device details', value: 'Fire TV OS 7.6.1.2' },
      { id: 'help', title: 'Help & Support', icon: HelpCircle, description: 'Get help and contact support', value: '' },
      { id: 'reset', title: 'Factory Reset', icon: Monitor, description: 'Reset device to factory settings', value: '' }
    ]
  }
];

const SettingsPage = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Settings</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {settingsCategories.map((category) => (
            <div key={category.title} className="bg-fire-dark rounded-xl p-6">
              <h2 className="text-2xl font-semibold text-white mb-6">{category.title}</h2>
              <div className="space-y-4">
                {category.items.map((item) => {
                  const Icon = item.icon;
                  return (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-4 bg-fire-gray/30 rounded-lg hover:bg-fire-orange/20 cursor-pointer transition-all duration-200 group"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-fire-orange/20 rounded-lg flex items-center justify-center">
                          <Icon size={24} className="text-fire-orange" />
                        </div>
                        <div>
                          <h3 className="text-white font-medium">{item.title}</h3>
                          <p className="text-gray-400 text-sm">{item.description}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {item.value && (
                          <span className="text-gray-300 text-sm">{item.value}</span>
                        )}
                        <ChevronRight size={20} className="text-gray-400 group-hover:text-fire-orange transition-colors" />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
