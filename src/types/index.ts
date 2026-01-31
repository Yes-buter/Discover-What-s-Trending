export interface GithubProject {
  id: number;
  repo_id: string;
  name: string;
  full_name: string;
  description: string | null;
  language: string | null;
  stars: number;
  forks: number;
  url: string;
  trending_date: string;
}

export interface Paper {
  id: string;
  title: string;
  abstract: string;
  authors: string[];
  pdf_url: string | null;
  code_url: string | null;
  published_date: string;
  source: string;
  category_id: string | null;
}

export interface Category {
  id: string;
  name: string;
  description: string | null;
  slug: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

export interface User {
  id: string;
  username: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserSignup extends UserLogin {
  username: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Favorite {
  id: string;
  user_id: string;
  item_type: 'project' | 'paper';
  item_id: string;
  created_at: string;
}
