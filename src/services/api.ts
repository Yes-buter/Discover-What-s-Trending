import axios from 'axios';
import { GithubProject, Paper, PaginatedResponse, Category, User, Token, UserLogin, UserSignup, Favorite } from '../types';

const API_URL = import.meta.env.PROD ? '/api' : '/api';


const api = axios.create({
  baseURL: API_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getTrendingProjects = async (params: {
  language?: string;
  since?: string;
  page?: number;
  limit?: number;
}) => {
  const response = await api.get<PaginatedResponse<GithubProject>>('/github/trending', { params });
  return response.data;
};

export const getProjectDetails = async (id: number) => {
  const response = await api.get<GithubProject>(`/github/${id}`);
  return response.data;
};

export const getLatestPapers = async (params: {
  category?: string;
  source?: string;
  page?: number;
  limit?: number;
}) => {
  const response = await api.get<PaginatedResponse<Paper>>('/papers/latest', { params });
  return response.data;
};

export const getPaperDetails = async (id: string) => {
  const response = await api.get<Paper>(`/papers/${id}`);
  return response.data;
};

export const getCategories = async () => {
  const response = await api.get<Category[]>('/papers/categories');
  return response.data;
};

// Auth API
export const login = async (data: UserLogin) => {
  const response = await api.post<Token>('/auth/login', data);
  return response.data;
};

export const signup = async (data: UserSignup) => {
  const response = await api.post<Token>('/auth/signup', data);
  return response.data;
};

// User API
export const getFavorites = async () => {
  const response = await api.get<Favorite[]>('/user/favorites');
  return response.data;
};

export const getEnrichedFavorites = async () => {
  const response = await api.get<{
    projects: GithubProject[];
    papers: Paper[];
  }>('/user/favorites/enriched');
  return response.data;
};

export const addFavorite = async (itemType: 'project' | 'paper', itemId: string) => {
  const response = await api.post<Favorite>('/user/favorites', { item_type: itemType, item_id: itemId });
  return response.data;
};

export const removeFavorite = async (itemType: 'project' | 'paper', itemId: string) => {
  const response = await api.delete(`/user/favorites/${itemType}/${itemId}`);
  return response.data;
};

// Admin API
export const triggerCrawl = async () => {
  const response = await api.post('/admin/crawl');
  return response.data;
};
