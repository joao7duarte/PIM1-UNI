#include <stdio.h>
#include "../routes/menuprof.h"
#include "../routes/menualuno.h"

void menuProfessor();
void menuAluno();

int main() {
    int usuario;
    do {
        printf("==== SISTEMA ESCOLAR ====\n");
        printf("1. Logar como professor\n");
        printf("2. Logar como aluno\n");
        printf("0. Sair\n");
        printf("Opcao: ");
        scanf("%d", &usuario);
        getchar(); 

        switch(usuario) {
            case 1: menuProfessor(); break;
            case 2: menuAluno(); break;
            case 0: printf("Encerrando o sistema...\n"); break;
            default: printf("Opcao invalida!\n");
        }

    } while(usuario != 0);

    return 0;
}


void menuProfessor() {
    int opcao;
    do {
        printf("\n===== SISTEMA PROFESSOR =====\n");
        printf("1. Cadastrar aluno\n");
        printf("2. Listar alunos\n");
        printf("3. Atualizar aluno\n");
        printf("4. Excluir aluno\n");
        printf("5. Lancar nota\n"); 
        printf("0. Voltar\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar(); 

        switch(opcao) {
            case 1: cadastrarAluno(); break;
            case 2: listarAlunos(); break;
            case 3: atualizarAluno(); break;
            case 4: excluirAluno(); break;
            case 5: lancarNota(); break; 
            case 0: break;
            default: printf("Opcao invalida!\n");
        }

    } while(opcao != 0);
}
void menuAluno() {
    int opcao;
    do {
        printf("\n===== SISTEMA ALUNO =====\n");
        printf("1. Ver notas\n");
        printf("0. Voltar\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);
        getchar(); 

        switch(opcao) {
            case 1: verNota(); break;
            case 0: break;
            default: printf("Opcao invalida!\n");
        }

    } while(opcao != 0);
}
