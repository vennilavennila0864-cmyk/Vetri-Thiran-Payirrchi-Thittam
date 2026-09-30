import { useState } from "react";

const API = "http://localhost:8000/api";

const templates = [
  ["employment", "Employment Agreement"],
  ["nda", "Non-Disclosure Agreement"],
  ["lease", "Lease Agreement"],
  ["consulting", "Consulting Agreement"],
];

export default function App() {
  const [type, setType] = useState("employment");
  const [title, setTitle] = useState("My Legal Document");
  const [fields, setFields] = useState({
    employer_name: "",
    employee_name: "",
    job_title: "",
    start_date: "",
    salary: "",
    governing_law: ""
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const update = (key: string, value: string) =>
    setFields(prev => ({ ...prev, [key]: value }));

  async function generate() {
    setLoading(true);
    try {
      const response = await fetch(`${API}/documents/generate`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ title, document_type: type, data: fields })
      });
      const data = await response.json();
      setResult(data.document);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <div>
          <h1>LegalEase</h1>
          <p>AI-Powered Legal Document Generator</p>
        </div>
        <span className="badge">AI Assisted</span>
      </header>

      <main>
        <section className="card">
          <h2>Create Document</h2>

          <label>Document Type</label>
          <select value={type} onChange={e => setType(e.target.value)}>
            {templates.map(([id, name]) => <option key={id} value={id}>{name}</option>)}
          </select>

          <label>Document Title</label>
          <input value={title} onChange={e => setTitle(e.target.value)} />

          <label>Employer / Party 1</label>
          <input value={fields.employer_name} onChange={e => update("employer_name", e.target.value)} />

          <label>Employee / Party 2</label>
          <input value={fields.employee_name} onChange={e => update("employee_name", e.target.value)} />

          <label>Job Title / Purpose</label>
          <input value={fields.job_title} onChange={e => update("job_title", e.target.value)} />

          <label>Effective Date</label>
          <input type="date" value={fields.start_date} onChange={e => update("start_date", e.target.value)} />

          <label>Salary / Consideration</label>
          <input value={fields.salary} onChange={e => update("salary", e.target.value)} />

          <label>Governing Law</label>
          <input value={fields.governing_law} onChange={e => update("governing_law", e.target.value)} />

          <button onClick={generate} disabled={loading}>
            {loading ? "Generating..." : "Generate Document"}
          </button>
        </section>

        <section className="card preview">
          <div className="preview-header">
            <h2>Preview</h2>
            {result && (
              <div>
                <a href={`${API}/documents/1/export/pdf`} target="_blank">PDF</a>
                {" · "}
                <a href={`${API}/documents/1/export/docx`} target="_blank">DOCX</a>
                {" · "}
                <a href={`${API}/documents/1/export/txt`} target="_blank">TXT</a>
              </div>
            )}
          </div>

          {!result && <div className="empty">Your generated document will appear here.</div>}

          {result && (
            <>
              <h1>{result.title}</h1>
              {result.sections.map((section: any) => (
                <article key={section.heading}>
                  <h3>{section.heading}</h3>
                  <p>{section.content}</p>
                </article>
              ))}

              <h3>Terms</h3>
              <table>
                <tbody>
                  {result.terms.map((term: any) => (
                    <tr key={term.term}><td>{term.term}</td><td>{term.value}</td></tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </section>
      </main>

      <footer>
        LegalEase is an AI-assisted drafting tool. Review generated documents with a qualified legal professional where appropriate.
      </footer>
    </div>
  );
}
