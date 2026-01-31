import { useEffect, useState } from 'react';
import { Star, GitFork, ExternalLink, Heart } from 'lucide-react';
import { getTrendingProjects, addFavorite, removeFavorite, getFavorites } from '../services/api';
import { GithubProject, Favorite } from '../types';
import { useAuth } from '../context/AuthContext';

const GithubTrending = () => {
  const [projects, setProjects] = useState<GithubProject[]>([]);
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState<string>('');
  const { user } = useAuth();

  useEffect(() => {
    fetchProjects();
    if (user) {
      fetchFavorites();
    }
  }, [language, user]);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const data = await getTrendingProjects({ 
        language: language || undefined,
        limit: 20 
      });
      setProjects(data.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFavorites = async () => {
    try {
      const data = await getFavorites();
      setFavorites(data);
    } catch (error) {
      console.error('Error fetching favorites:', error);
    }
  };

  const toggleFavorite = async (project: GithubProject) => {
    if (!user) {
      alert('Please log in to add favorites');
      return;
    }

    const isFav = favorites.some(f => f.item_id === project.id.toString() && f.item_type === 'project');
    
    try {
      if (isFav) {
        await removeFavorite('project', project.id.toString());
        setFavorites(favorites.filter(f => !(f.item_id === project.id.toString() && f.item_type === 'project')));
      } else {
        const newFav = await addFavorite('project', project.id.toString());
        setFavorites([...favorites, newFav]);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-3xl font-bold text-gray-900">GitHub Trending</h1>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="block w-full sm:w-48 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
        >
          <option value="">All Languages</option>
          <option value="Python">Python</option>
          <option value="JavaScript">JavaScript</option>
          <option value="TypeScript">TypeScript</option>
          <option value="Go">Go</option>
          <option value="Rust">Rust</option>
        </select>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => {
            const isFav = favorites.some(f => f.item_id === project.id.toString() && f.item_type === 'project');
            return (
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
                      <button
                        onClick={() => toggleFavorite(project)}
                        className={`p-1 rounded-full ${isFav ? 'text-red-500' : 'text-gray-400 hover:text-red-500'}`}
                      >
                        <Heart className={`w-5 h-5 ${isFav ? 'fill-current' : ''}`} />
                      </button>
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
            );
          })}
          {projects.length === 0 && (
            <div className="col-span-full text-center py-12 text-gray-500">
              No projects found.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default GithubTrending;
