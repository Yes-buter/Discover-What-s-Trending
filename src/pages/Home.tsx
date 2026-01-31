import { Link } from 'react-router-dom';
import { ArrowRight, Github, FileText } from 'lucide-react';

const Home = () => {
  return (
    <div className="space-y-10">
      {/* Hero Section */}
      <div className="bg-white rounded-lg shadow-sm p-8 text-center">
        <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
          Discover What's Trending
        </h1>
        <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
          Your daily dose of the hottest GitHub projects and cutting-edge Computer Vision research.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Link
            to="/github"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
          >
            <Github className="w-5 h-5 mr-2" />
            Explore Projects
          </Link>
          <Link
            to="/papers"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200"
          >
            <FileText className="w-5 h-5 mr-2" />
            Read Papers
          </Link>
        </div>
      </div>

      {/* Feature Sections */}
      <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
        <div className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-900">GitHub Trending</h2>
            <Link to="/github" className="text-blue-600 hover:text-blue-800 flex items-center">
              View All <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          <p className="text-gray-500 mb-4">
            Stay updated with the most starred repositories across various programming languages.
          </p>
          {/* Placeholder for preview content */}
          <div className="h-48 bg-gray-100 rounded-md flex items-center justify-center text-gray-400">
            Top Projects Preview
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-900">CV Papers</h2>
            <Link to="/papers" className="text-blue-600 hover:text-blue-800 flex items-center">
              View All <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          <p className="text-gray-500 mb-4">
            Access the latest research papers in Computer Vision from ArXiv and top conferences.
          </p>
          {/* Placeholder for preview content */}
          <div className="h-48 bg-gray-100 rounded-md flex items-center justify-center text-gray-400">
            Latest Papers Preview
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
