#include <stdio.h>
#include <string.h>
#include "../routes/menuprof.h"

#define ARQ_ALUNOS "database/alunos.txt"
#define MAX_ALUNOS 100

void cadastrarAluno() {
    Aluno aluno;
    aluno.nota = -1.0; // Nota padrão

    printf("Nome: ");
    fgets(aluno.nome, 100, stdin);
    aluno.nome[strcspn(aluno.nome, "\n")] = 0;

    printf("Email: ");
    fgets(aluno.email, 100, stdin);
    aluno.email[strcspn(aluno.email, "\n")] = 0;

    printf("Idade: ");
    scanf("%d", &aluno.idade);
    getchar();

    FILE *arquivo = fopen(ARQ_ALUNOS, "a");
    if (!arquivo) {
        printf("Erro ao abrir arquivo!\n");
        return;
    }

    fprintf(arquivo, "%s;%s;%d;%.2f\n", aluno.nome, aluno.email, aluno.idade, aluno.nota);
    fclose(arquivo);

    printf("Aluno cadastrado com sucesso!\n");
}

void listarAlunos() {
    Aluno aluno;
    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    
    if (!arquivo) {
        printf("Nenhum aluno cadastrado ainda.\n");
        return;
    }

    printf("\n===== LISTA DE ALUNOS =====\n");
    while (fscanf(arquivo, "%99[^;];%99[^;];%d;%f\n", 
                  aluno.nome, aluno.email, &aluno.idade, &aluno.nota) == 4) {
        printf("Nome: %s\n", aluno.nome);
        printf("Email: %s\n", aluno.email);
        printf("Idade: %d\n", aluno.idade);
        if (aluno.nota >= 0) {
            printf("Nota: %.2f\n", aluno.nota);
        } else {
            printf("Nota: Não lançada\n");
        }
        printf("---------------------------\n");
    }
    fclose(arquivo);
}

void atualizarAluno() {
    char emailBusca[100];
    Aluno alunos[MAX_ALUNOS];
    int total = 0;
    int encontrado = 0;

    printf("Digite o email do aluno a ser atualizado: ");
    fgets(emailBusca, 100, stdin);
    emailBusca[strcspn(emailBusca, "\n")] = 0;

    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (!arquivo) {
        printf("Nenhum aluno cadastrado ainda.\n");
        return;
    }

    while (fscanf(arquivo, "%99[^;];%99[^;];%d;%f\n",
                  alunos[total].nome, alunos[total].email, 
                  &alunos[total].idade, &alunos[total].nota) == 4) {
        total++;
    }
    fclose(arquivo);

    for (int i = 0; i < total; i++) {
        if (strcmp(alunos[i].email, emailBusca) == 0) {
            printf("Aluno encontrado!\n");
            printf("Novo nome: ");
            fgets(alunos[i].nome, 100, stdin);
            alunos[i].nome[strcspn(alunos[i].nome, "\n")] = 0;

            printf("Novo email: ");
            fgets(alunos[i].email, 100, stdin);
            alunos[i].email[strcspn(alunos[i].email, "\n")] = 0;

            encontrado = 1;
            break;
        }
    }

    if (!encontrado) {
        printf("Aluno não encontrado.\n");
        return;
    }

    arquivo = fopen(ARQ_ALUNOS, "w");
    if (!arquivo) {
        printf("Erro ao atualizar arquivo!\n");
        return;
    }

    for (int i = 0; i < total; i++) {
        fprintf(arquivo, "%s;%s;%d;%.2f\n", 
                alunos[i].nome, alunos[i].email, 
                alunos[i].idade, alunos[i].nota);
    }
    fclose(arquivo);

    printf("Aluno atualizado com sucesso!\n");
}

void excluirAluno() {
    char emailBusca[100];
    Aluno alunos[MAX_ALUNOS];
    int total = 0;
    int encontrado = 0;

    printf("Digite o email do aluno a ser excluido: ");
    fgets(emailBusca, 100, stdin);
    emailBusca[strcspn(emailBusca, "\n")] = 0;

    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (!arquivo) {
        printf("Nenhum aluno cadastrado ainda.\n");
        return;
    }

    Aluno temp;
    while (fscanf(arquivo, "%99[^;];%99[^;];%d;%f\n",
                  temp.nome, temp.email, &temp.idade, &temp.nota) == 4) {
        if (strcmp(temp.email, emailBusca) != 0) { 
            alunos[total++] = temp;
        } else {
            encontrado = 1;
        }
    }
    fclose(arquivo);

    if (!encontrado) {
        printf("Aluno não encontrado.\n");
        return;
    }

    arquivo = fopen(ARQ_ALUNOS, "w");
    if (!arquivo) {
        printf("Erro ao atualizar arquivo!\n");
        return;
    }

    for (int i = 0; i < total; i++) {
        fprintf(arquivo, "%s;%s;%d;%.2f\n", 
                alunos[i].nome, alunos[i].email, 
                alunos[i].idade, alunos[i].nota);
    }
    fclose(arquivo);

    printf("Aluno excluido com sucesso!\n");
}

void lancarNota() {
    char emailBusca[100];
    float novaNota;
    Aluno alunos[MAX_ALUNOS];
    int total = 0;
    int encontrado = 0;

    printf("Digite o email do aluno: ");
    fgets(emailBusca, 100, stdin);
    emailBusca[strcspn(emailBusca, "\n")] = 0;

    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (!arquivo) {
        printf("Nenhum aluno cadastrado ainda.\n");
        return;
    }

    while (fscanf(arquivo, "%99[^;];%99[^;];%d;%f\n",
                  alunos[total].nome, alunos[total].email,
                  &alunos[total].idade, &alunos[total].nota) == 4) {
        total++;
    }
    fclose(arquivo);

    for (int i = 0; i < total; i++) {
        if (strcmp(alunos[i].email, emailBusca) == 0) {
            printf("Aluno encontrado: %s\n", alunos[i].nome);
            printf("Digite a nota (0-10): ");
            scanf("%f", &novaNota);
            getchar();
            
            if (novaNota < 0 || novaNota > 10) {
                printf("Erro: Nota deve estar entre 0 e 10!\n");
                return;
            }
            alunos[i].nota = novaNota;
            encontrado = 1;
            break;
        }
    }

    if (!encontrado) {
        printf("Aluno não encontrado.\n");
        return;
    }

    arquivo = fopen(ARQ_ALUNOS, "w");
    if (!arquivo) {
        printf("Erro ao atualizar arquivo!\n");
        return;
    }

    for (int i = 0; i < total; i++) {
        fprintf(arquivo, "%s;%s;%d;%.2f\n",
                alunos[i].nome, alunos[i].email,
                alunos[i].idade, alunos[i].nota);
    }
    fclose(arquivo);

    printf("Nota lançada com sucesso!\n");
}