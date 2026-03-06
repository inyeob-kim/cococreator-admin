import { useState } from 'react';
import { useNavigate } from 'react-router';
import { LogIn } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // 간단한 로그인 처리 (실제로는 백엔드 인증 필요)
    if (email && password) {
      navigate('/dashboard');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-orange-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-600 rounded-2xl mb-4">
            <span className="text-white font-bold text-2xl">CC</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">CocoCreator Admin</h1>
          <p className="text-gray-600">크리에이터 브랜드 운영 시스템</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">로그인</h2>
          
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                이메일
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@cococreator.com"
                className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                비밀번호
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                required
              />
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-orange-600 border-gray-300 rounded focus:ring-orange-500"
                />
                <span className="ml-2 text-sm text-gray-600">로그인 상태 유지</span>
              </label>
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-orange-500 to-orange-600 text-white py-3 rounded-lg font-medium hover:from-orange-600 hover:to-orange-700 transition-all flex items-center justify-center gap-2"
            >
              <LogIn className="w-5 h-5" />
              로그인
            </button>
          </form>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-8">
          © 2026 CocoCreator. All rights reserved.
        </p>
      </div>
    </div>
  );
}