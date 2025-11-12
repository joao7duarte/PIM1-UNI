#include <stdio.h>
#include <string.h>
#include "../routes/menualuno.h"
#include "../routes/menuprof.h" 

#define ARQ_ALUNOS "database/alunos.txt"

void verNota() {
    char nome[100], email[100], emailBusca[100];
    int idade;
    float nota;
    int encontrado = 0;

    printf("Digite seu email para ver a nota: ");
    scanf("%99s", emailBusca);
    getchar();

    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (!arquivo) {
        printf("Nenhuma nota registrada ainda.\n");
        return;
    }

    while (fscanf(arquivo, "%99[^;];%99[^;];%d;%f\n", email, nome, &idade, &nota) == 4) {
        if (strcmp(email, emailBusca) == 0) {
            if (nota >= 0) {
                printf("Sua nota é: %.2f\n", nota);
            } else {
                printf("Nota não lançada ainda.\n");
            }
            encontrado = 1;
            break;
        }
    }
    fclose(arquivo);

    if (!encontrado)
        printf("Nota não encontrada para o email informado.\n");
}