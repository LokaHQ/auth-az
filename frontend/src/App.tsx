import type { Component } from 'solid-js';
import BooksList from './BooksList';

const App: Component = () => {
  return (
    <>
      <h1>List of books:</h1>
      <BooksList />
    </>
  );
};

export default App;
