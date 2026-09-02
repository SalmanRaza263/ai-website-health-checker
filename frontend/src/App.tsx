import React from 'react';
import Home from './Home';
// CSS files are loaded by the bundler and do not have TypeScript declarations.
// @ts-expect-error Bundler-provided stylesheet import.
import './styles/globals.css';
// @ts-expect-error Bundler-provided stylesheet import.
import './styles/animations.css';

function App() {
  return React.createElement(
    'div',
    { className: 'App' },
    React.createElement(Home),
  );
}

export default App;