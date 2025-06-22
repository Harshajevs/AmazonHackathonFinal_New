
import React from 'react';
import { Clock, Film, Smartphone, TrendingUp, Calendar, Award, Users, Activity } from 'lucide-react';

const DashboardPage = () => {
  const stats = [
    {
      title: 'Total Watch Time',
      value: '247 hours',
      subtitle: 'This month',
      icon: Clock,
      color: 'bg-blue-500',
      trend: '+12%'
    },
    {
      title: 'Movies Watched',
      value: '156',
      subtitle: 'All time',
      icon: Film,
      color: 'bg-green-500',
      trend: '+8'
    },
    {
      title: 'Favorite Genre',
      value: 'Action',
      subtitle: '42% of viewing',
      icon: Award,
      color: 'bg-purple-500',
      trend: null
    },
    {
      title: 'Active Subscriptions',
      value: '5',
      subtitle: 'Platforms',
      icon: Smartphone,
      color: 'bg-orange-500',
      trend: '+1'
    }
  ];

  const topApps = [
    { name: 'Netflix', hours: '89h', percentage: 78 },
    { name: 'Prime Video', hours: '67h', percentage: 58 },
    { name: 'YouTube', hours: '45h', percentage: 39 },
    { name: 'Hotstar', hours: '23h', percentage: 20 },
    { name: 'Aha', hours: '12h', percentage: 10 }
  ];

  const recentFeatures = [
    { feature: 'Watch Party', lastUsed: '2 hours ago', icon: Users },
    { feature: 'Playlist Creator', lastUsed: '1 day ago', icon: Film },
    { feature: 'Search', lastUsed: '2 days ago', icon: Activity },
    { feature: 'Settings', lastUsed: '1 week ago', icon: Activity }
  ];

  const weeklyData = [
    { day: 'Mon', hours: 3.5 },
    { day: 'Tue', hours: 2.8 },
    { day: 'Wed', hours: 4.2 },
    { day: 'Thu', hours: 3.1 },
    { day: 'Fri', hours: 5.6 },
    { day: 'Sat', hours: 7.2 },
    { day: 'Sun', hours: 6.8 }
  ];

  const maxHours = Math.max(...weeklyData.map(d => d.hours));

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold text-white">Dashboard</h1>
          <div className="flex items-center space-x-2 text-gray-400">
            <Calendar size={20} />
            <span>Last 30 days</span>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="bg-fire-dark rounded-xl p-6 hover:bg-fire-gray/20 transition-colors">
                <div className="flex items-center justify-between mb-4">
                  <div className={`w-12 h-12 ${stat.color} rounded-lg flex items-center justify-center`}>
                    <Icon size={24} className="text-white" />
                  </div>
                  {stat.trend && (
                    <span className="text-green-400 text-sm font-medium flex items-center">
                      <TrendingUp size={14} className="mr-1" />
                      {stat.trend}
                    </span>
                  )}
                </div>
                <h3 className="text-2xl font-bold text-white mb-1">{stat.value}</h3>
                <p className="text-gray-400 text-sm">{stat.subtitle}</p>
                <p className="text-gray-300 text-sm mt-2">{stat.title}</p>
              </div>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Weekly Activity */}
          <div className="bg-fire-dark rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-6">Weekly Activity</h3>
            <div className="space-y-4">
              {weeklyData.map((day, index) => (
                <div key={index} className="flex items-center justify-between">
                  <span className="text-gray-300 w-8">{day.day}</span>
                  <div className="flex-1 mx-4">
                    <div className="w-full bg-fire-gray/30 rounded-full h-2">
                      <div 
                        className="bg-fire-orange h-2 rounded-full transition-all duration-300"
                        style={{ width: `${(day.hours / maxHours) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <span className="text-gray-300 text-sm w-12 text-right">{day.hours}h</span>
                </div>
              ))}
            </div>
          </div>

          {/* Top Used Apps */}
          <div className="bg-fire-dark rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-6">Top Used Apps</h3>
            <div className="space-y-4">
              {topApps.map((app, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-fire-orange/20 rounded-lg flex items-center justify-center">
                      <span className="text-fire-orange text-sm font-bold">{index + 1}</span>
                    </div>
                    <span className="text-white font-medium">{app.name}</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-20 bg-fire-gray/30 rounded-full h-2">
                      <div 
                        className="bg-fire-orange h-2 rounded-full transition-all duration-300"
                        style={{ width: `${app.percentage}%` }}
                      ></div>
                    </div>
                    <span className="text-gray-300 text-sm w-8 text-right">{app.hours}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recently Accessed Features */}
          <div className="bg-fire-dark rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-6">Recently Accessed Features</h3>
            <div className="space-y-4">
              {recentFeatures.map((item, index) => {
                const Icon = item.icon;
                return (
                  <div key={index} className="flex items-center justify-between p-3 bg-fire-gray/20 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-fire-orange/20 rounded-lg flex items-center justify-center">
                        <Icon size={18} className="text-fire-orange" />
                      </div>
                      <span className="text-white font-medium">{item.feature}</span>
                    </div>
                    <span className="text-gray-400 text-sm">{item.lastUsed}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-fire-dark rounded-xl p-6">
            <h3 className="text-xl font-semibold text-white mb-6">Quick Actions</h3>
            <div className="grid grid-cols-2 gap-4">
              <button className="bg-fire-orange/20 hover:bg-fire-orange/30 text-fire-orange py-4 px-4 rounded-lg transition-colors flex flex-col items-center space-y-2">
                <Users size={24} />
                <span className="text-sm font-medium">Create Room</span>
              </button>
              <button className="bg-fire-orange/20 hover:bg-fire-orange/30 text-fire-orange py-4 px-4 rounded-lg transition-colors flex flex-col items-center space-y-2">
                <Film size={24} />
                <span className="text-sm font-medium">New Playlist</span>
              </button>
              <button className="bg-fire-orange/20 hover:bg-fire-orange/30 text-fire-orange py-4 px-4 rounded-lg transition-colors flex flex-col items-center space-y-2">
                <Activity size={24} />
                <span className="text-sm font-medium">View History</span>
              </button>
              <button className="bg-fire-orange/20 hover:bg-fire-orange/30 text-fire-orange py-4 px-4 rounded-lg transition-colors flex flex-col items-center space-y-2">
                <Smartphone size={24} />
                <span className="text-sm font-medium">Manage Apps</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
