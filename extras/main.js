const { Plugin, Modal, Notice } = require('obsidian');

class SheetImportModal extends Modal {
  constructor(app, onSubmit) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h2', { text: 'Paste SHEET Cheatsheet' });
    contentEl.createEl('p', { text: 'Paste your Markdown below and click Import.' });

    const textArea = contentEl.createEl('textarea', {
      attr: { rows: 10, cols: 50, placeholder: 'Paste your SHEET Markdown here...' }
    });

    const buttonDiv = contentEl.createEl('div', { cls: 'modal-button-container' });
    const importButton = buttonDiv.createEl('button', { text: 'Import' });
    importButton.addEventListener('click', () => {
      this.onSubmit(textArea.value);
      this.close();
    });

    textArea.focus();
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

module.exports = class SheetCollapsePlugin extends Plugin {
  async onload() {
    this.addCommand({
      id: 'import-sheet-collapsed',
      name: 'Import SHEET Cheatsheet (Collapsed)',
      editorCallback: (editor, view) => {
        new SheetImportModal(this.app, (markdown) => {
          try {
            if (!markdown.trim()) {
              new Notice('No Markdown provided!');
              return;
            }

            // Append the pasted content
            const lines = markdown.split('\n');
            const currentContent = editor.getValue();
            const newContent = currentContent ? `${currentContent}\n\n${markdown}` : markdown;
            editor.setValue(newContent);

            console.log('Lines imported:', lines.length);

            // Delay to ensure content renders, then fold all headings and lists
            setTimeout(() => {
              this.app.commands.executeCommandById('editor:fold-all');
              new Notice('SHEET cheatsheet imported and collapsed!');
            }, 200); // 200ms delay

          } catch (error) {
            new Notice(`Error importing cheatsheet: ${error.message}`);
            console.error(error);
          }
        }).open();
      }
    });
  }
};