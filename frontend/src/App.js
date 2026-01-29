import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

function App() {
  const { t, i18n } = useTranslation();
  const [lang, setLang] = useState('en');
  const [form, setForm] = useState({
    given_name: '', family_name: '', age: 30, weight_kg: '', allergies: '', current_medications: '', symptoms: ''
  });

  const switchLang = (l) => {
    i18n.changeLanguage(l);
    setLang(l);
    document.documentElement.dir = l === 'ar' ? 'rtl' : 'ltr';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    alert('Submit: use backend endpoint with basic auth (see README)');
  };

  return (
    <div style={{ padding: 20 }}>
      <div>
        <button onClick={() => switchLang('en')}>EN</button>
        <button onClick={() => switchLang('ar')}>AR</button>
      </div>
      <h1>{t('title')}</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Given name</label>
          <input value={form.given_name} onChange={e=>setForm({...form,given_name:e.target.value})} />
        </div>
        <div>
          <label>Family name</label>
          <input value={form.family_name} onChange={e=>setForm({...form,family_name:e.target.value})} />
        </div>
        <div>
          <label>Age</label>
          <input type="number" value={form.age} onChange={e=>setForm({...form,age:parseInt(e.target.value||0)})} />
        </div>
        <div>
          <label>Allergies (comma)</label>
          <input value={form.allergies} onChange={e=>setForm({...form,allergies:e.target.value})} />
        </div>
        <div>
          <label>Current medications</label>
          <input value={form.current_medications} onChange={e=>setForm({...form,current_medications:e.target.value})} />
        </div>
        <div>
          <label>Symptoms</label>
          <textarea value={form.symptoms} onChange={e=>setForm({...form,symptoms:e.target.value})} />
        </div>
        <button type="submit">{t('submit')}</button>
      </form>
    </div>
  );
}

export default App;
