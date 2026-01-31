import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { User, LogOut, Star, GitFork, ExternalLink, Calendar, Download, Code } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { getEnrichedFavorites } from '../services/api';
import { GithubProject, Paper } from '../types';

const Profile = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [favorites, setFavorites] = useState<{ projects: GithubProject[], papers: Paper[] }>({ projects: [], papers: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      fetchFavorites();
    }
  }, [user]);

  const fetchFavorites = async () => {
    try {
      const data = await getEnrichedFavorites();
      setFavorites(data);
    } catch (error) {
      console.error('Error fetching favorites:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) {
    return (
      <div className="flex justify-center items-center h-full">
        <p>Please log in to view your profile.</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-8 pb-12">
      <h1 className="text-3xl font-bold text-gray-900">User Profile</h1>
      
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-blue-100 p-3 rounded-full">
              <User className="w-8 h-8 text-blue-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">{user.username}</h2>
              {user.email && <p className="text-gray-500">{user.email}</p>}
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            <LogOut className="w-4 h-4 mr-2" />
            Sign Out
          </button>
        </div>
      </div>

      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Favorite Projects</h2>
        {loading ? (
           <div className="text-center py-4">Loading...</div>
        ) : favorites.projects.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {favorites.projects.map((project) => (
              <div key={project.id} className="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow">
                <div className="p-5">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900 truncate">
                      <a href={project.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
                        {project.name}
                      </a>
                    </h3>
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {project.language}
                      </span>
                    </div>
                  </div>
                  <p className="mt-2 text-sm text-gray-500 line-clamp-3 h-10">
                    {project.description}
                  </p>
                  <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
                    <div className="flex space-x-4">
                      <span className="flex items-center">
                        <Star className="w-4 h-4 mr-1 text-yellow-400" />
                        {project.stars.toLocaleString()}
                      </span>
                      <span className="flex items-center">
                        <GitFork className="w-4 h-4 mr-1" />
                        {project.forks.toLocaleString()}
                      </span>
                    </div>
                    <a
                      href={project.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No favorite projects yet.</p>
        )}
      </div>

      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Favorite Papers</h2>
        {loading ? (
           <div className="text-center py-4">Loading...</div>
        ) : favorites.papers.length > 0 ? (
          <div className="space-y-4">
            {favorites.papers.map((paper) => (
              <div key={paper.id} className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex flex-col md:flex-row md:justify-between md:gap-4">
                  <div className="flex-1">
                    <div className="flex justify-between items-start">
                      <h3 className="text-xl font-semibold text-gray-900">
                        {paper.title}
                      </h3>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-2 text-sm text-gray-500">
                      <span className="font-medium text-gray-700">Authors:</span>
                      {paper.authors.join(', ')}
                    </div>
                    <p className="mt-3 text-gray-600 line-clamp-2">
                      {paper.abstract}
                    </p>
                    <div className="mt-4 flex items-center gap-4 text-sm text-gray-500">
                      <span className="flex items-center">
                        <Calendar className="w-4 h-4 mr-1" />
                        {paper.published_date}
                      </span>
                      <span className="px-2 py-1 bg-gray-100 rounded text-xs uppercase tracking-wide">
                        {paper.source}
                      </span>
                    </div>
                  </div>
                  <div className="mt-4 md:mt-0 flex md:flex-col gap-2">
                    {paper.pdf_url && (
                      <a
                        href={paper.pdf_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 w-full md:w-auto"
                      >
                        <Download className="w-4 h-4 mr-2" />
                        PDF
                      </a>
                    )}
                    {paper.code_url && (
                      <a
                        href={paper.code_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 w-full md:w-auto"
                      >
                        <Code className="w-4 h-4 mr-2" />
                        Code
                      </a>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No favorite papers yet.</p>
        )}
      </div>
    </div>
  );
};

export default Profile;
