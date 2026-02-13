import { useEffect, useState } from 'react';
import { FileText, Download, Code, Calendar, Heart, RefreshCcw } from 'lucide-react';
import { getLatestPapers, getCategories, addFavorite, removeFavorite, getFavorites, triggerCrawl } from '../services/api';
import { Paper, Category, Favorite } from '../types';
import { useAuth } from '../context/AuthContext';

const CVPapers = () => {
  const [papers, setPapers] = useState<Paper[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const { user } = useAuth();

  useEffect(() => {
    fetchCategories();
  }, []);

  useEffect(() => {
    fetchPapers();
    if (user) {
      fetchFavorites();
    }
  }, [selectedCategory, user]);

  const fetchCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data || []);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchPapers = async () => {
    setLoading(true);
    try {
      const data = await getLatestPapers({ 
        category: selectedCategory || undefined,
        limit: 20 
      });
      setPapers(data.data);
    } catch (error) {
      console.error('Error fetching papers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await triggerCrawl();
      await new Promise(resolve => setTimeout(resolve, 3000));
      await fetchPapers();
    } catch (error) {
      console.error('Error refreshing data:', error);
    } finally {
      setRefreshing(false);
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

  const toggleFavorite = async (paper: Paper) => {
    if (!user) {
      alert('Please log in to add favorites');
      return;
    }

    const isFav = favorites.some(f => f.item_id === paper.id && f.item_type === 'paper');
    
    try {
      if (isFav) {
        await removeFavorite('paper', paper.id);
        setFavorites(favorites.filter(f => !(f.item_id === paper.id && f.item_type === 'paper')));
      } else {
        const newFav = await addFavorite('paper', paper.id);
        setFavorites([...favorites, newFav]);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-3xl font-bold text-gray-900">Computer Vision Papers</h1>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="block w-full sm:w-64 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
        >
          <option value="">All Categories</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className="space-y-4">
          {papers.map((paper) => {
            const isFav = favorites.some(f => f.item_id === paper.id && f.item_type === 'paper');
            return (
              <div key={paper.id} className="bg-white shadow rounded-lg p-6 hover:shadow-md transition-shadow">
                <div className="flex flex-col md:flex-row md:justify-between md:gap-4">
                  <div className="flex-1">
                    <div className="flex justify-between items-start">
                      <h3 className="text-xl font-semibold text-gray-900">
                        {paper.title}
                      </h3>
                      <button
                        onClick={() => toggleFavorite(paper)}
                        className={`p-1 rounded-full ${isFav ? 'text-red-500' : 'text-gray-400 hover:text-red-500'}`}
                      >
                        <Heart className={`w-5 h-5 ${isFav ? 'fill-current' : ''}`} />
                      </button>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-2 text-sm text-gray-500">
                      <span className="font-medium text-gray-700">Authors:</span>
                      {paper.authors.join(', ')}
                    </div>
                    <p className="mt-3 text-gray-600 line-clamp-3">
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
            );
          })}
          {papers.length === 0 && (
            <div className="flex flex-col items-center justify-center py-12 text-gray-500">
              <p className="mb-4">No papers found for the selected criteria.</p>
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                <RefreshCcw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
                {refreshing ? 'Refreshing...' : 'Refresh Data'}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CVPapers;
