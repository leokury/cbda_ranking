(async () => {
  const idEvento = "v1_JJrJSc7YOU0gdmvCxD7kwFPWxnEnU_Pp3t6tL3HV1iA.tzd-C8oQKsVvzzphdywCOdnYSPp5nmmi8viQPeBsUZQ";
  const categorias = [
    { id: "geral", nome: "Geral (Todas as Categorias)", param: "" },
    { id: "21",    nome: "Pré-Mirim",                    param: "21" },
    { id: "6",     nome: "Mirim 1",                       param: "6" },
    { id: "7",     nome: "Mirim 2",                       param: "7" },
    { id: "8",     nome: "Petiz 1",                       param: "8" },
    { id: "9",     nome: "Petiz 2",                       param: "9" }
  ];

  const resultado = {};

  for (const cat of categorias) {
    console.log(`Baixando ${cat.nome}...`);
    const res = await fetch(`https://www.cbda.org.br/api/pontuacao/clube?id_evento=${idEvento}&sexo=&id_classe=${cat.param}`, {
      credentials: "include"
    });
    const json = await res.json();
    resultado[cat.id] = json?.items?.items || [];
  }

  const blob = new Blob([JSON.stringify(resultado, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "dados_cbda.json";
  a.click();
  console.log("Arquivo dados_cbda.json atualizado e gerado com sucesso!");
})();