import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
import GithubTrending from './pages/GithubTrending';
import CVPapers from './pages/CVPapers';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Profile from './pages/Profile';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="github" element={<GithubTrending />} />
          <Route path="papers" element={<CVPapers />} />
          <Route path="profile" element={<Profile />} />
          {/* Add more routes as needed */}
          <Route path="*" element={<div className="p-8 text-center">Page not found</div>} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
