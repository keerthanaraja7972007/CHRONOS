import { jsPDF } from "jspdf";

export type ExportFormat = "markdown" | "json" | "text" | "pdf";

export function downloadBlob(filename: string, content: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

export function exportArtifact(title: string, body: string, format: ExportFormat) {
  const safeTitle = title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
  if (format === "json") {
    downloadBlob(`${safeTitle}.json`, JSON.stringify(body, null, 2), "application/json");
    return;
  }

  if (format === "pdf") {
    const doc = new jsPDF({ unit: "pt", format: "a4" });
    const lines = doc.splitTextToSize(body, 500);
    doc.setFontSize(12);
    doc.text(lines, 40, 40);
    doc.save(`${safeTitle}.pdf`);
    return;
  }

  if (format === "markdown") {
    downloadBlob(`${safeTitle}.md`, body, "text/markdown;charset=utf-8");
    return;
  }

  downloadBlob(`${safeTitle}.txt`, body, "text/plain;charset=utf-8");
}
