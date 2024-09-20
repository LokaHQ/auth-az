import { createSignal, onMount } from "solid-js";
import constants from './constants'

export default () => {
  let [books, setBooks] = createSignal([]);
  onMount(async () => {
    let response = await fetch(constants.backendHost + '/books');
    setBooks(await response.json())
  })
  return <table>
    {books().map(book => <tr><td><b>ID: </b>{book.id}</td><td><b>TITLE: </b>{book.title}</td></tr>)}
  </table>;
};
