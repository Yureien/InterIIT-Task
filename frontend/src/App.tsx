import React, { useEffect, useState, useRef } from 'react';
import './App.scss';

import { Container, Form } from 'react-bootstrap';
import MeiliSearch from 'meilisearch';
import { MEILI_CONFIG, MEILI_INDEX } from './config';
import { Result } from './data';
import ResultCard from './components/ResultCard/ResultCard';

function App() {
  const meiliClient = useRef<MeiliSearch>();
  const [hits, setHits] = useState<Result[] | undefined>();

  useEffect(() => {
    meiliClient.current = new MeiliSearch(MEILI_CONFIG);
  }, []);

  const search = async (e: React.FormEvent<HTMLInputElement>) => {
    if (meiliClient.current === undefined) {
      alert("MeiliSearch client not initialized! How even?");
      return;
    };

    const searchText = e.currentTarget.value;
    if (searchText.length < 3) {
      setHits(undefined);
      return;
    }
    const results = await meiliClient.current.index(MEILI_INDEX).search(searchText);
    console.log(results.hits);
    setHits(results.hits as Result[]);
  };

  let hitsComponent: JSX.Element | undefined;
  if (hits !== undefined) {
    if (hits.length === 0) {
      hitsComponent = <p>No results found!</p>;
    } else {
      hitsComponent = (
        <ul>
          {hits.map((hit) => <ResultCard result={hit} key={hit.id} />)}
        </ul>
      );
    }
  }

  return (
    <Container>
      <div className="d-flex flex-column align-items-center search-container">
        <h1 className="logo-text">Not Google</h1>
        <Form.Control className="search-input" type="text" placeholder="Search..." size="lg" onInput={search} />
      </div>
      <div className='d-flex flex-column align-items-center results-container'>
        {hitsComponent}
      </div>
    </Container>
  );
}

export default App;
