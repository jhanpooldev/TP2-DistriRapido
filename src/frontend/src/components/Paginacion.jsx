/** Controles de paginacion reutilizables por las tablas del panel. */
export default function Paginacion({
  page = 1,
  pages = 0,
  total = 0,
  onChange,
  etiqueta = 'registros',
}) {
  if (pages <= 1) {
    return <p className="texto-suave paginacion">{total} {etiqueta} en total.</p>
  }

  return (
    <nav className="btn-grupo paginacion" aria-label={`Paginacion de ${etiqueta}`}>
      <button
        type="button"
        className="btn-secondary btn-sm"
        onClick={() => onChange(page - 1)}
        disabled={page <= 1}
      >
        Anterior
      </button>
      <span className="texto-suave" aria-live="polite">
        Pagina {page} de {pages} · {total} {etiqueta}
      </span>
      <button
        type="button"
        className="btn-secondary btn-sm"
        onClick={() => onChange(page + 1)}
        disabled={page >= pages}
      >
        Siguiente
      </button>
    </nav>
  )
}
