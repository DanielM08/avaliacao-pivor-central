/**
 * Substitui window.storage (API do ambiente de artefatos)
 * por localStorage, para rodar no navegador local.
 */
if (typeof window !== "undefined" && !window.storage) {
  window.storage = {
    async get(key) {
      const value = localStorage.getItem(key);
      return value != null ? { value } : null;
    },
    async set(key, value) {
      localStorage.setItem(key, String(value));
      return true;
    },
  };
}
