#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "menuprof.h"

#define ARQ_ALUNOS "arquivos/alunos.txt"

#define MAX_ALUNOS 100

void lancarNota() {
    char email[100];
    float nota;
    int encontrado = 0;

    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (arquivo == NULL) {
        printf("Nenhum aluno cadastrado ainda.\n");
        return;
    }

    Aluno listaAlunos[MAX_ALUNOS];
    int totalAlunos = 0;

    while (fscanf(arquivo, "%99[^;];%99[^;];%d;%f",
                  listaAlunos[totalAlunos].email,
                  listaAlunos[totalAlunos].nome,
                  &listaAlunos[totalAlunos].idade,
                  &listaAlunos[totalAlunos].nota) >= 3)
    {
        listaAlunos[totalAlunos].email[strcspn(listaAlunos[totalAlunos].email, "\r\n")] = '\0';
        listaAlunos[totalAlunos].nome[strcspn(listaAlunos[totalAlunos].nome, "\r\n")] = '\0';
        totalAlunos++;
    }
    fclose(arquivo);

    printf("Digite o email do aluno: ");
    scanf("%99s", email);
    email[strcspn(email, "\r\n")] = '\0';

    for (int i = 0; i < totalAlunos; i++) {

        if (strcmp(listaAlunos[i].email, email) == 0) {
            printf("Digite a nota do aluno %s: ", listaAlunos[i].nome);
            scanf("%f", &nota);
            listaAlunos[i].nota = nota;
            printf("Nota registrada com sucesso!\n");
            encontrado = 1;
            break;
        }
    }

    if (!encontrado) {
        printf("Aluno nao encontrado!\n");
        return;
    }

    arquivo = fopen(ARQ_ALUNOS, "w");
    if (arquivo == NULL) {
        printf("Erro ao salvar as notas!\n");
        return;
    }

    for (int i = 0; i < totalAlunos; i++) {
        fprintf(arquivo, "%s;%s;%d;%.2f\n",
                listaAlunos[i].email,
                listaAlunos[i].nome,
                listaAlunos[i].idade,
                listaAlunos[i].nota);
    }

    fclose(arquivo);
}

void cadastrarAluno() {
    FILE *arquivo = fopen(ARQ_ALUNOS, "a");
    if (arquivo == NULL) {
        printf("Erro ao abrir arquivo!\n");
        return;
    }

    Aluno a;
    printf("Email do aluno: ");
    scanf("%99s", a.email);
    getchar(); 
    printf("Nome do aluno: ");
    fgets(a.nome, 100, stdin);
    a.nome[strcspn(a.nome, "\n")] = '\0';
    printf("Idade: ");
    scanf("%d", &a.idade);

    fprintf(arquivo, "%s;%s;%d\n", a.email, a.nome, a.idade);
    fclose(arquivo);

    printf("Aluno cadastrado com sucesso!\n");
}

void listarAlunos() {
    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (arquivo == NULL) {
        printf("Nenhum aluno cadastrado ainda.\n");
        return;
    }

    Aluno a;
    int campos;
    printf("\n--- Lista de Alunos ---\n");

    while (1) {
        
        campos = fscanf(arquivo, "%99[^;];%99[^;];%d", a.email, a.nome, &a.idade);
        if (campos != 3) break; 

        campos = fscanf(arquivo, ";%f\n", &a.nota);
        if (campos != 1) a.nota = -1; 

        printf("Email: %s | Nome: %s | Idade: %d | ", a.email, a.nome, a.idade);
        if (a.nota < 0)
            printf("Nota: ainda nao lancada\n");
        else
            printf("Nota: %.2f\n", a.nota);
    }

    fclose(arquivo);
}

void atualizarAluno() {
    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (arquivo == NULL) {
        printf("Nenhum aluno cadastrado.\n");
        return;
    }

    FILE *temp = fopen("arquivos/temp.txt", "w");
    if (temp == NULL) {
        printf("Erro ao criar arquivo temporario.\n");
        fclose(arquivo);
        return;
    }

    char emailBusca[100];
    printf("Digite o email do aluno que deseja atualizar: ");
    scanf("%99s", emailBusca);
    getchar();

    Aluno a;
    int encontrado = 0;

    while (fscanf(arquivo, "%99[^;];%99[^;];%d\n", a.email, a.nome, &a.idade) == 3) {
        if (strcmp(a.email, emailBusca) == 0) {
            encontrado = 1;
            printf("Novo nome: ");
            fgets(a.nome, 100, stdin);
            a.nome[strcspn(a.nome, "\n")] = '\0';
            printf("Nova idade: ");
            scanf("%d", &a.idade);
        }
        fprintf(temp, "%s;%s;%d\n", a.email, a.nome, a.idade);
    }

    fclose(arquivo);
    fclose(temp);

    remove(ARQ_ALUNOS);
    rename("arquivos/temp.txt", ARQ_ALUNOS);

    if (encontrado)
        printf("Aluno atualizado com sucesso!\n");
    else
        printf("Aluno nao encontrado.\n");
}


void excluirAluno() {
    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (arquivo == NULL) {
        printf("Nenhum aluno cadastrado.\n");
        return;
    }

    FILE *temp = fopen("arquivos/temp.txt", "w");
    if (temp == NULL) {
        printf("Erro ao criar arquivo temporario.\n");
        fclose(arquivo);
        return;
    }

    char emailBusca[100];
    printf("Digite o email do aluno que deseja excluir: ");
    scanf("%99s", emailBusca);
    getchar();

    Aluno a;
    int encontrado = 0;

    while (fscanf(arquivo, "%99[^;];%99[^;];%d\n", a.email, a.nome, &a.idade) == 3) {
        if (strcmp(a.email, emailBusca) == 0) {
            encontrado = 1;
            continue; 
        }
        fprintf(temp, "%s;%s;%d\n", a.email, a.nome, a.idade);
    }

    fclose(arquivo);
    fclose(temp);

    remove(ARQ_ALUNOS);
    rename("arquivos/temp.txt", ARQ_ALUNOS);

    if (encontrado)
        printf("Aluno excluido com sucesso!\n");
    else
        printf("Aluno nao encontrado.\n");
}
