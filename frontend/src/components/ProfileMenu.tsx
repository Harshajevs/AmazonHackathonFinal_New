
import React, { useState } from 'react';
import { User, ChevronDown, LogOut, UserCheck } from 'lucide-react';

const ProfileMenu = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 p-2 rounded-full bg-fire-gray/50 hover:bg-fire-gray transition-colors duration-200"
      >
        <div className="w-8 h-8 bg-fire-orange rounded-full flex items-center justify-center">
          <User size={16} className="text-white" />
        </div>
        <ChevronDown size={16} className="text-white" />
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute right-0 top-12 w-48 bg-fire-dark rounded-lg shadow-lg border border-fire-gray/30 z-20">
            <div className="p-3 border-b border-fire-gray/30">
              <p className="text-white font-medium">Praneeth JV</p>
              <p className="text-gray-400 text-sm">praneeth.jvp@gmail.com</p>
            </div>
            <div className="py-2">
              <button className="w-full px-4 py-2 text-left text-white hover:bg-fire-gray/50 flex items-center space-x-2 transition-colors duration-200">
                <UserCheck size={16} />
                <span>Switch Account</span>
              </button>
              <button className="w-full px-4 py-2 text-left text-white hover:bg-fire-gray/50 flex items-center space-x-2 transition-colors duration-200">
                <LogOut size={16} />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ProfileMenu;
