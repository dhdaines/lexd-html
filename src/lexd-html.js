class LexdDefinition extends HTMLElement {
    connectedCallback() {
        const shadow = this.attachShadow({ mode: "open" });
        shadow.innerHTML = `<style>
table {
	table-layout: fixed;
	width: 80%;
	margin: 0.5em;
	border: 1px solid;
}
thead th { border-block-end: 1px solid; }
td, th { text-align: left; }
</style>`;
        for (const table of this.querySelectorAll("table")) {
            const sec = table.getAttribute("data-section");
            if (!sec) continue;
            const secHeader = sec.toUpperCase();
            const name = table.getAttribute("data-name") ?? "";
            let colspan = 0;
            for (const row of table.rows)
                colspan = Math.max(colspan, row.cells.length);
            table.createTHead().innerHTML = `
<tr><th colspan="${colspan}">${secHeader} ${name}</th></tr>
`;
            shadow.append(table);
        }
    }
}

window.customElements.define("lexd-definition", LexdDefinition);
