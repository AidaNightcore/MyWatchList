import { AutoComplete } from "primereact/autocomplete";
import { useState, useEffect } from "react";
import api from "../../../services/api";

const PublisherAutocomplete = ({ value, onChange }) => {
  const [options, setOptions] = useState([]);
  const [filtered, setFiltered] = useState([]);

  useEffect(() => {
    api
      .get("api/media/publishers")
      .then((res) => setOptions(Array.isArray(res.data) ? res.data : []))
      .catch(() => setOptions([]));
  }, []);

  const search = (e) => {
    const query = e.query?.toLowerCase() || "";
    const list = Array.isArray(options) ? options : [];
    setFiltered(list.filter((g) => g.name.toLowerCase().includes(query)));
  };

  return (
    <AutoComplete
      value={value || []}
      suggestions={filtered}
      completeMethod={search}
      multiple
      dropdown
      virtualScrollerOptions={{ itemSize: 36, style: { height: "200px" } }}
      field="name"
      onChange={(e) => onChange(e.value)}
      placeholder="Publisheri"
      style={{ minWidth: 200 }}
    />
  );
};

export default PublisherAutocomplete;
